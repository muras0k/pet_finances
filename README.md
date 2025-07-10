# Finance Microservice (FastAPI + PostgreSQL)

A pet project for tracking personal expenses, built with FastAPI, PostgreSQL, Tailwind CSS, and Jinja2. Allows users to add, view, and delete expenses, as well as view spending statistics by category.

---

## Features

-  Add new expense with category, amount, and date
-  View monthly category-based statistics
-  Browse expenses by specific date
-  Delete expenses by ID
-  Web interface using HTML + Tailwind + Flowbite
-  API available under `/api/...` routes

---

##  Tech Stack

- **Backend:** FastAPI
- **Database:** PostgreSQL
- **Database Access:** Raw SQL via psycopg
- **Frontend:** Jinja2, TailwindCSS, Flowbite

---

## ⚙ Installation & Setup

### 1. Clone the project

git clone https://github.com/muras0k/pet_finances.git
cd pet_finances 

### 2. Create a virtual environment

python3 -m venv venv
source venv/bin/activate

### 3. Install dependencies

pip install -r requirements.txt

### 4. Set up the database

Make sure PostgreSQL is running
Create the expenses table:

CREATE TABLE expenses (
    id SERIAL PRIMARY KEY,
    amount FLOAT NOT NULL,
    category VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL
);

### 5. Run the app

uvicorn app.main:app --reload

Visit in browser:

    http://localhost:8000 — home page

    http://localhost:8000/add — add an expense

    http://localhost:8000/statistics — view statistics

    http://localhost:8000/api/expenses — raw API


📧 Author

Andrei Murashko


