import os

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.business_logic.exceptions import existence, validation
from src.api import handlers
from src.api.controllers import category
from src.api.controllers import task, authorization
from src.database.dependency import get_database_session_factory
from src.database.models import base


@pytest.fixture(scope="session")
def engine():
    database_url = os.environ.get("SQLALCHEMY_TEST_DATABASE_URL")
    engine = create_engine(database_url)
    yield engine
    engine.dispose()


@pytest.fixture
def tables(engine):
    base.Base.metadata.create_all(bind=engine)
    yield
    base.Base.metadata.drop_all(bind=engine)


@pytest.fixture
def session(engine, tables):
    with engine.connect() as connection:
        transaction = connection.begin()
        with Session(bind=engine) as session:
            yield session
            transaction.rollback()


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
def photo():
    with open("tests/profile.png", "rb") as f:
        return f.read()


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
        "name": "John"
    }
    client.post(url="api/authorization/signup", data=user_info)


@pytest.fixture
def daily_task(client, user):
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
