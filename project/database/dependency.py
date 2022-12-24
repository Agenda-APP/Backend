from typing import NoReturn, Iterator

from fastapi import Depends
from sqlalchemy.orm import sessionmaker, Session


def get_database_session_factory() -> NoReturn:
    raise NotImplementedError


def get_database_session(
    session_factory: sessionmaker = Depends(get_database_session_factory),
) -> Iterator[Session]:
    with session_factory() as session:
        yield session
