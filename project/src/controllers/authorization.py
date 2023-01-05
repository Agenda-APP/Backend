from fastapi import APIRouter, Depends, Form, UploadFile, status

from src.business_logic import providers
from src.business_logic.schemas.auth import LoginDetails, SignUpDetails, Token
from src.business_logic.services.auth import AuthService


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
    return auth_service.register_user(email, photo, name, password)


@router.post(
    "/login", response_model=Token, status_code=status.HTTP_201_CREATED
)
def login(
    user: LoginDetails,
    auth_service: AuthService = Depends(providers.auth_service_provider),
):
    return auth_service.login_user(user.email, user.password)
