from fastapi import APIRouter, Depends, HTTPException, status

from src import providers
from src.dto.task import CategoryDTO, TaskDTO
from src.errors import existence
from src.schemas.task import TaskCreation, TasksRead, TaskUpdate
from src.services.task import TaskService


router = APIRouter(prefix="/task", tags=["task"])


@router.post(
    "/create", status_code=status.HTTP_201_CREATED, response_model=TaskCreation
)
def create_task(
    task: TaskCreation,
    task_service: TaskService = Depends(providers.task_service_provider),
):
    try:
        task_service.create_new_task(
            TaskDTO(
                status=task.status,
                end_date=task.end_date,
                description=task.description,
                category=CategoryDTO(task.category),
                priority=task.priority,
            )
        )
    except existence.DoesNotExistError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category does not exist",
        )
    return {**task.dict()}


@router.delete("/delete/{task_id}", status_code=status.HTTP_200_OK)
def delete_task(
    task_id: int,
    task_service: TaskService = Depends(providers.task_service_provider),
):
    try:
        task_service.delete_existing_task(task_id=task_id)
    except existence.DoesNotExistError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task does not exist",
        )
    return {"message": "Task has been deleted"}


@router.put(
    "/update/{task_id}",
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
