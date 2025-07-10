from pydantic import BaseModel
from enum import Enum
from datetime import datetime
from typing import Optional

class Category(str, Enum):
    food = "Food"
    transport = "Transport"
    housing = "Housing"
    internet = "Internet"
    health = "Health"
    entertainment = "Entertainment"
    other = "Other"

class Expense(BaseModel):
    amount: float
    category: Category
    created_at: datetime
