import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.api import handlers
from src.business_logic.exceptions import existence, validation
from src.business_logic import providers
from src.api.controllers import category
from src.api.controllers import task, authorization
from src.database.dependency import get_database_session_factory
from src.database.provider import DatabaseProvider


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
    app.add_exception_handler(
        existence.AlreadyExistsError, handlers.already_exists_handler
    )
    app.add_exception_handler(
        existence.DoesNotExistError, handlers.does_not_exist_handler
    )
    app.add_exception_handler(
        validation.IncorrectDataError, handlers.incorrect_data_handler
    )
    configure_database(app)
    configure_routes(app)
    return app
