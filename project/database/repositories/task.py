from datetime import datetime

import sqlalchemy
from sqlalchemy.orm import Session, joinedload

from database.models import task
from src.enumerations import Priority, Status
from .repository import AbstractRepository
from src.dto.task import TaskDTO


class TaskRepository(AbstractRepository):
    def __init__(self, session: sqlalchemy.orm.Session):
        super().__init__(session)

    def create_task(
            self,
            user_id: int | None,
            description: str,
            category_id: int | None,
            status: Status,
            priority: Priority,
            end_date: datetime,
    ) -> None:
        query = sqlalchemy.insert(task.Task).values(
            user_id=user_id,
            description=description,
            category_id=category_id,
            status=status,
            priority=priority,
            end_date=end_date,
        )
        self.session.execute(query)
        self.session.commit()

    def delete_task(self, task_id: int) -> None:
        query = sqlalchemy.delete(task.Task).where(
            task.Task.id == task_id
        )
        self.session.execute(query)
        self.session.commit()

    def update_task(
            self, task_id: int, category_id: int | None, existing_task: TaskDTO
    ) -> task.Task | None:
        query = (
            sqlalchemy.update(task.Task).where(task.Task.id == task_id).values(
                description=existing_task.description,
                category_id=category_id,
                status=existing_task.status,
                priority=existing_task.priority,
                end_date=existing_task.end_date,
            )
        )
        self.session.execute(query)
        self.session.commit()
        updated = (self.session.execute(
            sqlalchemy.select(task.Task)
                      .where(task.Task.id == task_id)
                      .options(joinedload(task.Task.category))
        ))
        return updated.scalar()
