from fastapi import FastAPI, Request, Response, status, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from datetime import datetime, date
from pathlib import Path
import psycopg
from app.database import pool
from app.models import Expense, Category
from enum import Enum

templates = Jinja2Templates(directory=Path(__file__).parent / "templates")

app = FastAPI()

@app.get("/add", response_class=HTMLResponse)
def add_expenses(request: Request):
    return templates.TemplateResponse("add.html", {"request": request})

@app.get("/statistics", response_class=HTMLResponse)
async def statistics(request: Request):
    return templates.TemplateResponse("statistics.html", {"request":request}) # send html temlates

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request":request})

@app.post("/api/add")
def add_expense(expense: Expense):
    if expense.amount > 0:
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO expenses (amount, category, created_at)
                    VALUES (%s, %s, %s)
                    RETURNING *
                """, (expense.amount, expense.category, expense.created_at)) # if amount is correct add row in db
                new_expense = cur.fetchone()
            conn.commit()
    else:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)
     
    if new_expense:
        return Response(status_code=status.HTTP_201_CREATED)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.get("/api/distribution")
def get_diagram():
    with pool.connection() as conn:
        with conn.cursor() as cur:  #select all expenses from this month
            cur.execute("""
            SELECT * FROM expenses
            WHERE DATE_TRUNC('month', created_at) = DATE_TRUNC('month', CURRENT_DATE) 
            ORDER BY created_at DESC
            """)
            rows = cur.fetchall() #recieve all data from db
    expenses: list[Expense] = [
        Expense(id=row[0], amount=row[1], category=row[2], created_at=row[3]) #put data into expenses
        for row in rows
    ]
    total = sum(e.amount for e in expenses)# count sum of all amounts
    if total == 0:
        return{} #no expenses this month
        
    per_category = dict()
    for e in expenses:
        if e.category not in per_category:
            per_category[e.category] = 0.0
        per_category[e.category] += e.amount #create dict with all expens of 1 category

    percent_distribution = {
        category.name.lower(): round((amount / total) * 100, 2)
        for category, amount in per_category.items()
    }
    return JSONResponse(content=percent_distribution)

@app.get("/api/expenses")
def get_expenses(year: int, month: int, day: int):
    selected_date = date(year, month, day)  #insert values to one date variable
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            SELECT  id, category, amount, created_at
            FROM expenses
            WHERE DATE(created_at) = %s
            ORDER BY created_at DESC
            """, (selected_date,))  
            rows = cur.fetchall()
    result = [
        {   
            "id": row[0],
            "category": row[1],
            "amount": row[2],
            "date": row[3].strftime("%H:%M")
        }
        for row in rows
    ]
    return result

@app.delete("/api/expenses/{id}")
def del_expense(id: int):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            DELETE FROM expenses
            WHERE id = %s
            RETURNING *
            """,(id,))
            deleted_expense = cur.fetchone()
        conn.commit()
    if deleted_expense:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"expense with id: {id} not found")
