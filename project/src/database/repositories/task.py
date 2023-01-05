import sqlalchemy
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql import exists

from src.database.models import task
from src.business_logic.dto.task import TaskDTO
from .repository import AbstractRepository


class TaskRepository(AbstractRepository):
    def __init__(self, session: sqlalchemy.orm.Session):
        super().__init__(session)

    def create_task(
        self,
        task_dto: TaskDTO,
        category_id: int | None,
    ) -> None:
        query = sqlalchemy.insert(task.Task).values(
            user_id=task_dto.user_id,
            description=task_dto.description,
            category_id=category_id,
            status=task_dto.status,
            priority=task_dto.priority,
            end_date=task_dto.end_date,
        )
        self.session.execute(query)
        self.session.commit()

    def delete_task(self, task_id: int) -> None:
        query = sqlalchemy.delete(task.Task).where(task.Task.id == task_id)
        self.session.execute(query)
        self.session.commit()

    def update_task(
        self, task_id: int, category_id: int | None, existing_task: TaskDTO
    ) -> task.Task | None:
        query = (
            sqlalchemy.update(task.Task)
            .where(task.Task.id == task_id)
            .values(
                description=existing_task.description,
                category_id=category_id,
                status=existing_task.status,
                priority=existing_task.priority,
                end_date=existing_task.end_date,
            )
        )
        self.session.execute(query)
        self.session.commit()
        updated = self.session.execute(
            sqlalchemy.select(task.Task)
            .where(task.Task.id == task_id)
            .options(joinedload(task.Task.category))
        )
        return updated.scalar()

    def is_exists(self, task_id: int) -> bool:
        return self.session.query(
            exists().where(task.Task.id == task_id)
        ).scalar()
