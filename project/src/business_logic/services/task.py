from src.database.models import task
from src.database.repositories.category import CategoryRepository
from src.database.repositories.task import TaskRepository
from src.business_logic.dto.task import TaskDTO
from src.business_logic.errors import existence


class TaskService:
    def __init__(
        self,
        task_repository: TaskRepository,
        category_repository: CategoryRepository,
    ):
        self.task_repository = task_repository
        self.category_repository = category_repository

    def create_new_task(self, task_dto: TaskDTO) -> None:
        if self.category_repository is not None:
            category_id = self.category_repository.get_id_of_category(
                task_dto.category.name
            )
            if category_id is None:
                raise existence.DoesNotExistError
            self.task_repository.create_task(
                task_dto,
                category_id=category_id,
            )

    def delete_existing_task(self, task_id: int) -> None:
        if not self.task_repository.is_exists(task_id=task_id):
            raise existence.DoesNotExistError
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
