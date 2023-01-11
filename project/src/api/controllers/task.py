from fastapi import APIRouter, Depends, status

from src.business_logic import providers
from src.business_logic.dto.task import CategoryDTO, TaskDTO
from src.api.schemas.task import (
    TaskCreation,
    TasksRead,
    TaskUpdate,
    TaskCreatedRead,
    AllTasksRead
)
from src.business_logic.classes.authentication import Authentication
from src.business_logic.services.task import TaskService


router = APIRouter(tags=["task"])


@router.post(
    "/api/task",
    status_code=status.HTTP_201_CREATED,
    response_model=TaskCreatedRead,
)
def create_task(
    task: TaskCreation,
    task_service: TaskService = Depends(providers.task_service_provider),
):
    task_id = task_service.create_new_task(
        TaskDTO(
            user_id=task.user_id,
            status=task.status,
            end_date=task.end_date,
            description=task.description,
            category=CategoryDTO(task.category),
            priority=task.priority,
        )
    )
    return {**task.dict(), "id": task_id}


@router.delete("/api/task/{task_id}", status_code=status.HTTP_200_OK)
def delete_task(
    task_id: int,
    task_service: TaskService = Depends(providers.task_service_provider),
):
    task_service.delete_existing_task(task_id=task_id)
    return {"message": "Task has been deleted"}


@router.put(
    "/api/task/{task_id}",
    status_code=status.HTTP_200_OK,
    response_model=TasksRead,
)
def update_task(
    task_id: int,
    task: TaskUpdate,
    task_service: TaskService = Depends(providers.task_service_provider),
):
    updated_task = task_service.update_existing_task(
        task_id,
        TaskDTO(
            status=task.status,
            end_date=task.end_date,
            description=task.description,
            category=CategoryDTO(task.category.name),
            priority=task.priority,
        ),
    )
    return updated_task


@router.get(
    "/api/tasks/active/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=list[AllTasksRead],
    dependencies=[Depends(Authentication().requires_authentication)]
)
def get_active_tasks(user_id: int,
                     task_service: TaskService = Depends(providers.task_service_provider)):
    return task_service.get_active_tasks_of_user(user_id)


@router.get(
    "/api/tasks/done/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=list[AllTasksRead],
    dependencies=[Depends(Authentication().requires_authentication)]
)
def get_done_tasks(user_id: int,
                   task_service: TaskService = Depends(providers.task_service_provider)):
    return task_service.get_done_tasks_of_user(user_id)
