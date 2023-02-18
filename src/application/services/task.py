from business_logic.dto.task import TaskDTO
from business_logic.exceptions import existence
from database.models.task import Task
from database.repositories.category import CategoryRepository
from database.repositories.task import TaskRepository


class TaskService:
    def __init__(
        self,
        task_repository: TaskRepository,
        category_repository: CategoryRepository,
    ):
        self.task_repository = task_repository
        self.category_repository = category_repository

    def create_new_task(self, task_dto: TaskDTO) -> int | None:
        if self.category_repository is not None:
            category_id = self.category_repository.get_id_of_category(
                task_dto.category
            )
            if category_id is None:
                raise existence.DoesNotExistError(
                    "The category does not exist"
                )
            task_id = self.task_repository.create_task(
                task_dto,
                category_id=category_id,
            )
            return task_id
        return None

    def delete_existing_task(self, task_id: int) -> None:
        if not self.task_repository.is_exists(task_id=task_id):
            raise existence.DoesNotExistError("The task does not exist")
        self.task_repository.delete_task(task_id=task_id)

    def update_existing_task(
        self, task_id: int, task_dto: TaskDTO
    ) -> TaskDTO | None:
        if self.category_repository is not None:
            category_id = self.category_repository.get_id_of_category(
                task_dto.category
            )
            if category_id is None:
                raise existence.DoesNotExistError("Category does not exist")
            updated_task = self.task_repository.update_task(
                task_id=task_id,
                category_id=category_id,
                existing_task=task_dto,
            )
            return TaskDTO(*updated_task)
        return None

    def get_active_tasks_of_user(self, user_id: int) -> list[Task]:
        return self.task_repository.get_all_active_tasks_of_user(user_id)

    def get_done_tasks_of_user(self, user_id: int) -> list[Task]:
        return self.task_repository.get_all_done_tasks_of_user(user_id)
