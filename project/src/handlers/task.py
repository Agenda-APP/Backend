from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from database.dependency import get_database_session
from database.repositories.category import CategoryRepository
from database.repositories.task import TaskRepository
from src.schemas.task import TaskCreation, TaskUpdate, TasksRead
from src.services.task import TaskService
from src.errors import existence
from src.dto.task import TaskDTO, CategoryDTO


router = APIRouter(prefix="/task", tags=["task"])


@router.post(
    "/create", status_code=status.HTTP_201_CREATED, response_model=TaskCreation
)
def create_task(
    task: TaskCreation, session: Session = Depends(get_database_session)
):
    try:
        TaskService(
            TaskRepository(session), CategoryRepository(session)
        ).create_new_task(
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
    task_id: int, session: Session = Depends(get_database_session)
):
    TaskService(TaskRepository(session)).delete_existing_task(task_id=task_id)
    return {"message": "Task has been deleted"}


@router.put(
    "/update/{task_id}",
    status_code=status.HTTP_200_OK,
    response_model=TasksRead,
)
def update_task(
    task_id: int,
    task: TaskUpdate,
    session: Session = Depends(get_database_session),
):
    updated_task = TaskService(
        TaskRepository(session), CategoryRepository(session)
    ).update_existing_task(
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
