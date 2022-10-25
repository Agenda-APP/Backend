import os

import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from database.models import base
from database.dependency import get_database_session_factory
from src.endpoints.authorization import router


@pytest.fixture(scope="session")
def engine():
    database_url = os.environ.get("SQLALCHEMY_TEST_DATABASE_URL")
    engine = create_engine(database_url)
    yield engine
    engine.dispose()


@pytest.fixture(scope="session")
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
    app.include_router(router)
    app.dependency_overrides[get_database_session_factory] = lambda: lambda: session
    return app


@pytest.fixture
def client(app):
    with TestClient(app=app) as client:
        yield client


@pytest.fixture
def photo():
    with open("tests/profile.png", 'rb') as f:
        return f.read()
