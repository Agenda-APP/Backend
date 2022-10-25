from fastapi import APIRouter, Depends, HTTPException, UploadFile, Form, status
from sqlalchemy.orm import Session

import utilities
from database.repositories.user import UserRepository
from database.dependency import get_database_session
from src.classes.authorization import Authorization
from src.schemas.auth import SignUpDetails, Token, LoginDetails


router = APIRouter(
    prefix="/authorization",
    tags=["auth"]
)


@router.post("/signup", response_model=SignUpDetails, status_code=status.HTTP_201_CREATED)
def signup(email: str = Form(), password: str = Form(),
           name: str = Form(), photo: None | UploadFile = None,
           session: Session = Depends(get_database_session)):
    user_from_db = UserRepository(session).get_user_by_email(email=email)
    if user_from_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The email already exists")
    if photo is not None:
        utilities.save_photo(photo)
        UserRepository(session).create_user(email=email, name=name,
                                            password=password, photo=photo.filename)
        photo_url = f"localhost/static/photos/{photo.filename}"
        return {"message": "account successfully created", "email": email,
                "name": name, "photo_url": photo_url}
    UserRepository(session).create_user(email=email, name=name, password=password)
    return {"message": "account successfully created", "email": email, "name": name}


@router.post("/login", response_model=Token, status_code=status.HTTP_201_CREATED)
def login(user: LoginDetails, session: Session = Depends(get_database_session)):
    auth = Authorization()
    user_from_db = UserRepository(session).get_user_by_email(email=user.email)
    if user_from_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist",
            headers={"WWW-Authenticate": "Bearer"},
        )
    verified_password = auth.verify_password(user.password, user_from_db.password)
    if not verified_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect email or password")
    access_token = auth.create_access_token(user.email)
    return {"message": "login successfully", "email": user.email, "access_token": access_token}
