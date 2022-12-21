from datetime import datetime

import sqlalchemy
from sqlalchemy.orm import Session

from database.models import task
from src.enumerations import Priority, Status
from .repository import AbstractRepository


class TaskRepository(AbstractRepository):
    def __init__(self, session: sqlalchemy.orm.Session):
        super().__init__(session)

    def create_task(
        self,
        description: str,
        category: int | None,
        status: Status,
        priority: Priority,
        end_date: datetime,
    ) -> None:

        query = sqlalchemy.insert(task.Task).values(
            description=description,
            category=category,
            status=status,
            priority=priority,
            end_date=end_date,
        )
        self.session.execute(query)
        self.session.commit()

    def delete_task(self, description: str) -> None:
        query = sqlalchemy.delete(task.Task).where(
            task.Task.description == description
        )
        self.session.execute(query)
        self.session.commit()
