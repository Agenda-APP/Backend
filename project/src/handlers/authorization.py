from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile, status

from src import providers
from src.errors import existence, validation
from src.schemas.auth import LoginDetails, SignUpDetails, Token
from src.services.auth import AuthService


router = APIRouter(prefix="/api/authorization", tags=["auth"])


@router.post(
    "/signup",
    response_model=SignUpDetails,
    status_code=status.HTTP_201_CREATED,
)
def signup(
    email: str = Form(),
    password: str = Form(),
    name: str = Form(),
    photo: None | UploadFile = None,
    auth_service: AuthService = Depends(providers.auth_service_provider),
):
    try:
        response = auth_service.register_user(email, photo, name, password)
    except existence.AlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The email already exists",
        )
    return response


@router.post(
    "/login", response_model=Token, status_code=status.HTTP_201_CREATED
)
def login(
    user: LoginDetails,
    auth_service: AuthService = Depends(providers.auth_service_provider),
):
    try:
        response = auth_service.login_user(user.email, user.password)
    except existence.DoesNotExistError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except validation.IncorrectDataError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    return response
