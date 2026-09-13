from app.db.session import Base
from sqlalchemy import Column, Integer, String


class Expense(Base):
    __tablename__ = "expenses_mcp"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    description = Column(String, nullable=True)