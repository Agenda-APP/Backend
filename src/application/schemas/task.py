from datetime import datetime

from pydantic import BaseModel

from enumerations import Priority, Status


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
    user_id: int | None
    category: str | None

    class Config:
        orm_mode = True


class TaskUpdate(TaskBase):
    user_id: int
    category: str


class AllTasksRead(TaskBase):
    user_id: int
    id: int

    class Config:
        orm_mode = True
