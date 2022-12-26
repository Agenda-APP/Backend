from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from src.enumerations import Priority, Status
from src.schemas.category import Category


class TaskCreation(BaseModel):
    user_id: int
    description: str
    category: str
    status: Status
    priority: Priority
    end_date: datetime


class TaskDeletion(BaseModel):
    description: str


class TasksRead(BaseModel):
    id: int
    user_id: int
    status: Status
    end_date: datetime
    description: str
    category: Category
    priority: Priority

    class Config:
        orm_mode = True


class TaskUpdate(BaseModel):
    status: Optional[Status]
    end_date: Optional[datetime]
    description: Optional[str]
    category: Optional[Category]
    priority: Optional[Priority]
