from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker


def create_database_engine(database_url: str) -> Engine:
    return create_engine(url=database_url)


def create_session_factory(database_engine: Engine) -> sessionmaker:
    return sessionmaker(
        autocommit=False, autoflush=False, bind=database_engine
    )
