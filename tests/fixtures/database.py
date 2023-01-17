import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from database.models import base


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
