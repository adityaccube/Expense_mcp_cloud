from app.db.session import create_tables
from app.models.expense import Expense

create_tables()

print("Database tables created successfully")