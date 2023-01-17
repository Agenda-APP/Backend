import os

import pytest
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.testclient import TestClient

from application import handlers
from application.controllers import category
from application.controllers import task, authorization
from business_logic.exceptions import existence, validation
from database.dependency import get_database_session_factory


@pytest.fixture
def app(session):
    app = FastAPI()
    app.include_router(authorization.router)
    app.include_router(task.router)
    app.include_router(category.router)
    app.dependency_overrides[
        get_database_session_factory
    ] = lambda: lambda: session
    app.add_exception_handler(
        existence.AlreadyExistsError, handlers.already_exists_handler
    )
    app.add_exception_handler(
        existence.DoesNotExistError, handlers.does_not_exist_handler
    )
    app.add_exception_handler(
        validation.IncorrectDataError, handlers.incorrect_data_handler
    )
    return app


@pytest.fixture
def client(app):
    with TestClient(app=app) as client:
        yield client


@pytest.fixture
def created_category(client):
    new_category = {"name": "Основные"}
    response = client.post(url="api/category", json=new_category)
    return response


@pytest.fixture
def user(client):
    user_info = {
        "email": "test@mail.ru",
        "password": "somepassword",
        "name": "John",
    }
    client.post(url="api/authorization/signup", data=user_info)


@pytest.fixture
def daily_task(client, user, created_category):
    daily = {
        "user_id": 1,
        "description": "Пойти в магазин",
        "category": "Основные",
        "status": "Создано",
        "priority": "Срочно сделать",
        "end_date": "2022-12-03T16:28:08.464Z",
    }
    response = client.post(url="api/task", json=daily)
    return response


@pytest.fixture
def authorized_user(client):
    user_info = {
        "email": "test@mail.ru",
        "password": "somepassword",
        "name": "John",
    }
    login_info = {"email": "test@mail.ru", "password": "somepassword"}
    client.post(url="api/authorization/signup", data=user_info)
    response = client.post(url="api/authorization/login", json=login_info)
    return response.json()


@pytest.fixture
def done_task(client, user, created_category):
    daily = {
        "user_id": 1,
        "description": "Пойти в магазин",
        "category": "Основные",
        "status": "Завершено",
        "priority": "Срочно сделать",
        "end_date": "2022-12-03T16:28:08.464Z",
    }
    response = client.post(url="api/task", json=daily)
    return response
