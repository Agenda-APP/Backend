import os

import utilities
from database.repositories.user import UserRepository
from business_logic.authentication.auth import Authentication
from business_logic.exceptions import validation
from business_logic.exceptions import existence
from business_logic.dto.user import UserDTO
from business_logic.authentication.jwt_manager import JWTManager


class AuthService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def register_user(self, user_dto: UserDTO) -> dict:
        user_from_db = self.repository.get_user_by_email(email=user_dto.email)
        user_info = {"email": user_dto.email, "name": user_dto.name}
        if user_from_db:
            raise existence.AlreadyExistsError("The user already exists")
        if user_dto.photo is not None:
            photo_url = utilities.save_photo(user_dto.photo)
            user_id = self.repository.create_user(
                email=user_dto.email,
                name=user_dto.name,
                password=user_dto.password,
                photo=user_dto.photo.filename,
            )
            user_info["photo_url"] = photo_url
            user_info["user_id"] = user_id
            return user_info
        user_id = self.repository.create_user(
            email=user_dto.email,
            name=user_dto.name,
            password=user_dto.password,
        )
        user_info["user_id"] = user_id
        return user_info

    def login_user(self, user_dto: UserDTO) -> dict:
        jwt_manager = JWTManager(
            int(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"]),
            os.environ["SECRET"],
            os.environ["ALGORITHM"],
        )
        user_from_db = self.repository.get_user_by_email(email=user_dto.email)
        if user_from_db is None:
            raise existence.DoesNotExistError("User does not exist")
        verified_password = Authentication().verify_password(
            user_dto.password, user_from_db.password
        )
        if not verified_password:
            raise validation.IncorrectDataError("Incorrect email or password")
        access_token = jwt_manager.create_access_token(user_dto.email)
        return {"email": user_dto.email, "access_token": access_token}
