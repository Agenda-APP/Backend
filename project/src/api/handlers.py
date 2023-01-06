from fastapi import status
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from src.business_logic.exceptions import existence, validation


def already_exists_handler(
    _: Request, exception: existence.AlreadyExistsError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": exception.message},
    )


def does_not_exist_handler(
    _: Request, exception: existence.DoesNotExistError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": exception.message},
    )


def incorrect_data_handler(
    _: Request, exception: validation.IncorrectDataError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"message": exception.message},
    )
