from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, RelationshipProperty

from database.models.base import Base
from enumerations import Priority, Status


class Category(Base):
    __tablename__ = "categories"

    id: Column[Integer] = Column(Integer, primary_key=True)
    name: Column[String] = Column(String(120), nullable=False, unique=True)


class Task(Base):
    __tablename__ = "tasks"

    id: Column[Integer] = Column(Integer, primary_key=True)
    user_id: Column[Integer] = Column(
        Integer, ForeignKey(column="profiles.id", ondelete="CASCADE")
    )
    description: Column[String] = Column(String(120), nullable=False)
    category_id: Column[Integer] = Column(
        Integer, ForeignKey(column="categories.id", ondelete="CASCADE")
    )
    category: RelationshipProperty = relationship("Category", backref="tasks")
    status: Status = Column(Enum(Status))
    priority: Priority = Column(Enum(Priority))
    end_date: Column[DateTime] = Column(DateTime, nullable=False)
