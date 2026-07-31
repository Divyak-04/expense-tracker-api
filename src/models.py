"""
Pydantic models for the Smart Expense Tracker API.
"""
import datetime as dt
from pydantic import BaseModel, Field, field_validator


class ExpenseCreate(BaseModel):
    """Payload for creating a new expense. id is assigned by the server."""

    title: str = Field(..., min_length=1, description="Short description of the expense")
    amount: float = Field(..., gt=0, description="Amount spent, must be positive")
    category: str = Field(..., min_length=1, description="Expense category, e.g. 'food'")
    date: dt.date = Field(..., description="Date the expense occurred, format YYYY-MM-DD")

    @field_validator("title", "category")
    @classmethod
    def not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("must not be blank")
        return v.strip()


class Expense(ExpenseCreate):
    """An expense as stored and returned by the API (includes its id)."""

    id: int


class CategoryTotal(BaseModel):
    category: str
    total: float


class TotalsResponse(BaseModel):
    overall_total: float
    by_category: list[CategoryTotal]
