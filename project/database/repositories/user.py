from sqlalchemy.orm import Session

from database.models import user
from src.classes.authorization import Authorization
from .repository import Repository


class UserRepository(Repository):
    def __init__(self, session: Session):
        super().__init__(session)

    def get_user_by_email(self, email: str) -> user.Profile | None:
        current_user = (self.session.query(user.Profile)
                        .filter(user.Profile.email == email)
                        .first())
        return current_user

    def create_user(self, email: str, password: str,
                    name: str, photo: str | None = None) -> user.Profile | None:
        hashed_password = Authorization().get_hashed_password(password)
        created_user = user.Profile(email=email, password=hashed_password,
                                    name=name, photo=photo)
        self.session.add(created_user)
        self.session.commit()
        self.session.refresh(created_user)
        return created_user
