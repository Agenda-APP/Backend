import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.database.dependency import get_database_session_factory
from src.database.provider import DatabaseProvider
from src.business_logic import providers
from src.controllers import authorization, category, task


def configure_database(app: FastAPI) -> None:
    provider = DatabaseProvider(os.environ["SQLALCHEMY_DATABASE_URL"])
    app.dependency_overrides[
        get_database_session_factory
    ] = lambda: provider.session_factory


def configure_routes(app: FastAPI) -> None:
    app.include_router(authorization.router)
    app.include_router(task.router)
    app.include_router(category.router)


def create_app() -> FastAPI:
    app = FastAPI(
        title="Task Book", description="Convenient task management service"
    )
    app.mount("/static", StaticFiles(directory="src/static"), name="static")
    app.dependency_overrides[
        providers.task_service_factory
    ] = providers.task_service_provider
    app.dependency_overrides[
        providers.category_service_factory
    ] = providers.category_service_provider
    app.dependency_overrides[
        providers.auth_service_factory
    ] = providers.auth_service_provider
    configure_database(app)
    configure_routes(app)
    return app
