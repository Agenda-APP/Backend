from datetime import datetime

from pydantic import BaseModel
from src.enumerations import Priority, Status


class TaskCreation(BaseModel):
    description: str
    category: str
    status: Status
    priority: Priority
    end_date: datetime


class TaskDeletion(BaseModel):
    description: str
