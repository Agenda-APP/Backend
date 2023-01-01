from database.repositories.category import CategoryRepository
from database.repositories.task import TaskRepository
from database.models import task
from src.errors.existence import DoesNotExistError
from src.dto.task import TaskDTO


class TaskService:
    def __init__(
        self,
        task_repository: TaskRepository,
        category_repository: CategoryRepository | None = None,
    ):
        self.task_repository = task_repository
        self.category_repository = category_repository

    def create_new_task(self, task_dto: TaskDTO) -> None:
        if self.category_repository is not None:
            category_id = self.category_repository.get_id_of_category(
                task_dto.category.name
            )
            if category_id is None:
                raise DoesNotExistError
            self.task_repository.create_task(
                user_id=task_dto.user_id,
                description=task_dto.description,
                end_date=task_dto.end_date,
                category_id=category_id,
                priority=task_dto.priority,
                status=task_dto.status,
            )

    def delete_existing_task(self, task_id: int) -> None:
        self.task_repository.delete_task(task_id=task_id)

    def update_existing_task(
        self, task_id: int, task_dto: TaskDTO
    ) -> task.Task | None:
        if self.category_repository is not None:
            category_id = self.category_repository.get_id_of_category(
                task_dto.category.name
            )
            updated_task = self.task_repository.update_task(
                task_id=task_id,
                category_id=category_id,
                existing_task=task_dto,
            )
            return updated_task
        return None
