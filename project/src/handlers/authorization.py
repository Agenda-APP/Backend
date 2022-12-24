from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from database.dependency import get_database_session
from database.repositories.user import UserRepository
from src.errors import existence, validation
from src.schemas.auth import LoginDetails, SignUpDetails, Token
from src.services.auth import AuthService


router = APIRouter(prefix="/authorization", tags=["auth"])


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
    session: Session = Depends(get_database_session),
):
    try:
        response = AuthService(UserRepository(session)).register_user(
            email, photo, name, password
        )
        return response
    except existence.AlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The email already exists",
        )


@router.post(
    "/login", response_model=Token, status_code=status.HTTP_201_CREATED
)
def login(
    user: LoginDetails, session: Session = Depends(get_database_session)
):
    try:
        response = AuthService(UserRepository(session)).login_user(
            user.email, user.password
        )
        return response
    except existence.DoesNotExistsError:
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
