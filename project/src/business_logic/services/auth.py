from fastapi import UploadFile

from src import utilities
from src.database.repositories.user import UserRepository
from src.business_logic.authorization import Authorization
from src.business_logic.errors import validation
from src.business_logic.errors import existence
from src.business_logic.dto.user import UserDTO


class AuthService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def register_user(self, user_dto: UserDTO) -> dict:
        user_from_db = self.repository.get_user_by_email(email=user_dto.email)
        if user_from_db:
            raise existence.AlreadyExistsError("The user already exists")
        if user_dto.photo is not None:
            photo_url = utilities.save_photo(user_dto.photo)
            self.repository.create_user(
                email=user_dto.email,
                name=user_dto.name,
                password=user_dto.password,
                photo=user_dto.photo.filename,
            )
            return {
                "email": user_dto.email,
                "name": user_dto.name,
                "photo_url": photo_url,
            }
        self.repository.create_user(
            email=user_dto.email,
            name=user_dto.name,
            password=user_dto.password,
        )
        return {"email": user_dto.email, "name": user_dto.name}

    def login_user(self, user_dto: UserDTO) -> dict:
        auth = Authorization()
        user_from_db = self.repository.get_user_by_email(email=user_dto.email)
        if user_from_db is None:
            raise existence.DoesNotExistError("User does not exist")
        verified_password = auth.verify_password(
            user_dto.password, user_from_db.password
        )
        if not verified_password:
            raise validation.IncorrectDataError("Incorrect email or password")
        access_token = auth.create_access_token(user_dto.email)
        return {"email": user_dto.email, "access_token": access_token}
