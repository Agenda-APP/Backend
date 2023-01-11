from datetime import datetime

from pydantic import BaseModel

from src.enumerations import Priority, Status
from src.api.schemas.category import Category


class TaskBase(BaseModel):
    status: Status
    description: str
    end_date: datetime
    priority: Priority


class TaskCreation(TaskBase):
    user_id: int
    category: str


class TaskCreatedRead(TaskBase):
    id: int
    user_id: int
    category: str


class TasksRead(TaskBase):
    id: int
    user_id: int | None
    category: Category | None

    class Config:
        orm_mode = True


class TaskUpdate(TaskBase):
    category: Category


class AllTasksRead(TaskBase):
    user_id: int
    id: int

    class Config:
        orm_mode = True
