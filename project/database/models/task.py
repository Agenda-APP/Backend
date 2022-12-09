from datetime import datetime

from database.models.base import Base
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from src.enumerations import Priority, Status


class Category(Base):
    __tablename__ = "categories"

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(120), nullable=False, unique=True)
    task: relationship = relationship("Task")


class Task(Base):
    __tablename__ = "tasks"

    id: int = Column(Integer, primary_key=True)
    description: str = Column(String(120), nullable=False)
    category: int = Column(
        Integer, ForeignKey(column="categories.id", ondelete="CASCADE")
    )
    status: Status = Column(Enum(Status))
    priority: Priority = Column(Enum(Priority))
    end_date: datetime = Column(DateTime, nullable=False)
