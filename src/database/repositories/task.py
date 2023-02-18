import sqlalchemy as sa
from sqlalchemy.orm import Session
from sqlalchemy.engine import Row
from sqlalchemy.sql import exists

from business_logic.dto.task import TaskDTO
from database.models.task import Task, Category
from enumerations import Status
from .repository import AbstractRepository


class TaskRepository(AbstractRepository):
    def __init__(self, session: sa.orm.Session):
        super().__init__(session)

    def create_task(
            self,
            task_dto: TaskDTO,
            category_id: int | None,
    ) -> int | None:
        query = (
            sa.insert(Task)
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
        query = sa.delete(Task).where(Task.id == task_id)
        self.session.execute(query)
        self.session.commit()

    def update_task(
            self, task_id: int, category_id: int | None, existing_task: TaskDTO
    ) -> Row | None:  # TODO закоммитить изменения
        query = (
            sa.update(Task)
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
        updated_task_query = (sa.select(Task.user_id, Task.status, Task.end_date,
                       Task.description, Category.name.label("category"),
                       Task.priority)
             .join(Category)
             .where(Task.id == task_id))
        updated_task = self.session.execute(updated_task_query).first()
        return updated_task

    def is_exists(self, task_id: int) -> bool:
        return self.session.query(exists().where(Task.id == task_id)).scalar()

    def get_all_active_tasks_of_user(self, user_id: int) -> list[Task]:
        query = sa.select(Task).where(
            (Task.user_id == user_id) & (Task.status == Status.CREATED)
        )
        return self.session.execute(query).scalars().all()

    def get_all_done_tasks_of_user(self, user_id: int) -> list[Task]:
        query = sa.select(Task).where(
            (Task.user_id == user_id) & (Task.status == Status.DONE)
        )
        return self.session.execute(query).scalars().all()
