import sqlalchemy
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql import exists

from database.models.task import Task
from business_logic.dto.task import TaskDTO
from .repository import AbstractRepository
from enumerations import Status


class TaskRepository(AbstractRepository):
    def __init__(self, session: sqlalchemy.orm.Session):
        super().__init__(session)

    def create_task(
        self,
        task_dto: TaskDTO,
        category_id: int | None,
    ) -> int | None:
        query = (
            sqlalchemy.insert(Task)
            .values(
                user_id=task_dto.user_id,
                description=task_dto.description,
                category_id=category_id,
                status=task_dto.status,
                priority=task_dto.priority,
                end_date=task_dto.end_date,
            )
            .returning(Task.id)
        )
        result = self.session.execute(query)
        self.session.commit()
        task_id = result.scalar()
        return task_id

    def delete_task(self, task_id: int) -> None:
        query = sqlalchemy.delete(Task).where(Task.id == task_id)
        self.session.execute(query)
        self.session.commit()

    def update_task(
        self, task_id: int, category_id: int | None, existing_task: TaskDTO
    ) -> Task | None:
        query = (
            sqlalchemy.update(Task)
            .where(Task.id == task_id)
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
            sqlalchemy.select(Task)
            .where(Task.id == task_id)
            .options(joinedload(Task.category))
        )
        return updated.scalar()

    def is_exists(self, task_id: int) -> bool:
        return self.session.query(exists().where(Task.id == task_id)).scalar()

    def get_all_active_tasks_of_user(self, user_id: int) -> list[Task]:
        query = sqlalchemy.select(Task).where(
            (Task.user_id == user_id) & (Task.status == Status.CREATED)
        )
        return self.session.execute(query).scalars().all()

    def get_all_done_tasks_of_user(self, user_id: int) -> list[Task]:
        query = sqlalchemy.select(Task).where(
            (Task.user_id == user_id) & (Task.status == Status.DONE)
        )
        return self.session.execute(query).scalars().all()
