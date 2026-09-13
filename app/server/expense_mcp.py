#app/server/expense_mcp.py
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))


from fastmcp import FastMCP
from app.db.session import SessionLocal, create_tables
from app.models.expense import Expense

mcp = FastMCP(name="Expense Tracker")

create_tables()

@mcp.tool
def add_expense(
    title: str,
    amount: float,
    description: str,
):
    db = SessionLocal()

    try:
        expense = Expense(
            title=title,
            amount=amount,
            description=description,
        )

        db.add(expense)
        db.commit()
        db.refresh(expense)

        return {
            "title": expense.title,
            "amount": expense.amount,
            "description": expense.description,
        }

    finally:
        db.close()


@mcp.tool
def get_expenses():
    db = SessionLocal()

    try:
        expenses = db.query(Expense).all()

        return [
            {
                "title": expense.title,
                "amount": expense.amount,
                "description": expense.description,
            }
            for expense in expenses
        ]

    finally:
        db.close()

if __name__ == "__main__":
    mcp.run()