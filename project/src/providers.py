from typing import NoReturn

from fastapi import Depends
from sqlalchemy.orm import Session

from database.dependency import get_database_session
from database.repositories import category, task, user
from src.services.auth import AuthService
from src.services.category import CategoryService
from src.services.task import TaskService


def task_service_factory() -> NoReturn:
    raise NotImplementedError


def category_service_factory() -> NoReturn:
    raise NotImplementedError


def auth_service_factory() -> NoReturn:
    raise NotImplementedError


def task_service_provider(
    session: Session = Depends(get_database_session),
) -> TaskService:
    task_repository = task.TaskRepository(session)
    category_repository = category.CategoryRepository(session)
    return TaskService(
        task_repository=task_repository,
        category_repository=category_repository,
    )


def category_service_provider(
    session: Session = Depends(get_database_session),
) -> CategoryService:
    category_repository = category.CategoryRepository(session)
    return CategoryService(category_repository=category_repository)


def auth_service_provider(
    session: Session = Depends(get_database_session),
) -> AuthService:
    user_repository = user.UserRepository(session)
    return AuthService(repository=user_repository)
