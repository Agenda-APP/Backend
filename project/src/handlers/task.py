from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from database.dependency import get_database_session
from database.repositories.category import CategoryRepository
from database.repositories.task import TaskRepository
from src.schemas.task import TaskCreation, TaskDeletion
from src.services.task import TaskService
from src.errors import existence


router = APIRouter(prefix="/task", tags=["task"])


@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_task(
    task: TaskCreation, session: Session = Depends(get_database_session)
):
    task_repo = TaskRepository(session)
    category_repo = CategoryRepository(session)
    try:
        TaskService(task_repo, category_repo).create_new_task(
            description=task.description,
            end_date=task.end_date,
            category=task.category,
            priority=task.priority,
            status=task.status,
        )
    except existence.DoesNotExistsError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category does not exist",
        )
    return {"message": "Task has been created"}


@router.delete("/delete", status_code=status.HTTP_200_OK)
def delete_task(
    task: TaskDeletion, session: Session = Depends(get_database_session)
):
    task_repo = TaskRepository(session)
    TaskService(task_repo).delete_existing_task(description=task.description)
    return {"message": "Task has been deleted"}
