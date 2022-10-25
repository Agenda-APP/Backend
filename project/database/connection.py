from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def create_database_engine(db_url):
    return create_engine(url=db_url)


def create_session_factory(db_engine) -> sessionmaker:
    return sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
