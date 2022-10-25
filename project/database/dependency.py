from fastapi import Depends
from sqlalchemy.orm import sessionmaker


def get_database_session_factory() -> sessionmaker:
    raise NotImplementedError


def get_database_session(session_factory: sessionmaker = Depends(get_database_session_factory)):
    with session_factory() as session:
        yield session
