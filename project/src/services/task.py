from datetime import datetime

from database.repositories.category import CategoryRepository
from database.repositories.task import TaskRepository
from src import enumerations
from src.errors.existence import DoesNotExistsError


class TaskService:
    def __init__(
        self,
        task_repository: TaskRepository,
        category_repository: CategoryRepository | None = None,
    ):
        self.task_repository = task_repository
        self.category_repository = category_repository

    def create_new_task(
        self,
        user_id: int,
        description: str,
        end_date: datetime,
        category: str,
        priority: enumerations.Priority,
        status: enumerations.Status,
    ) -> None:
        if self.category_repository is not None:
            category_id = self.category_repository.get_id_of_category(category)
            if category_id is None:
                raise DoesNotExistsError
            self.task_repository.create_task(
                user_id=user_id,
                description=description,
                end_date=end_date,
                category_id=category_id,
                priority=priority,
                status=status,
            )

    def delete_existing_task(self, description: str) -> None:
        self.task_repository.delete_task(description=description)

    def update_existing_task(
            self, task_id: int, task
    ):
        category_id = self.category_repository.get_id_of_category(
            task.category.name
        )
        updated_task = self.task_repository.update_task(
            task_id=task_id, category_id=category_id, existing_task=task
        )
        return updated_task
