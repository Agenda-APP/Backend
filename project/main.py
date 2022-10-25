import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.endpoints import authorization
from database.provider import DatabaseProvider
from database.dependency import get_database_session_factory


app = FastAPI(title='Task Book')
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(authorization.router)

provider = DatabaseProvider(os.environ["SQLALCHEMY_DATABASE_URL"])
app.dependency_overrides[get_database_session_factory] = lambda: provider.session_factory
