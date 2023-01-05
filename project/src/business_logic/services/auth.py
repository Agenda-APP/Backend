from fastapi import UploadFile

from src import utilities
from src.database.repositories.user import UserRepository
from src.business_logic.authorization import Authorization
from src.business_logic.errors import validation
from src.business_logic.errors import existence


class AuthService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def register_user(
        self, email: str, photo: UploadFile | None, name: str, password: str
    ) -> dict:
        user_from_db = self.repository.get_user_by_email(email=email)
        if user_from_db:
            raise existence.AlreadyExistsError("Such user already exists")
        if photo is not None:
            photo_url = utilities.save_photo(photo)
            self.repository.create_user(
                email=email, name=name, password=password, photo=photo.filename
            )
            return {
                "message": "account successfully created",
                "email": email,
                "name": name,
                "photo_url": photo_url,
            }
        self.repository.create_user(email=email, name=name, password=password)
        return {
            "message": "account successfully created",
            "email": email,
            "name": name,
        }

    def login_user(self, email: str, password: str) -> dict:
        auth = Authorization()
        user_from_db = self.repository.get_user_by_email(email=email)
        if user_from_db is None:
            raise existence.DoesNotExistError("User does not exist")
        verified_password = auth.verify_password(
            password, user_from_db.password
        )
        if not verified_password:
            raise validation.IncorrectDataError("Incorrect email or password")
        access_token = auth.create_access_token(email)
        return {
            "message": "login successfully",
            "email": email,
            "access_token": access_token,
        }
