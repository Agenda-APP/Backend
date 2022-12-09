import sqlalchemy
from sqlalchemy.orm import Session

from database.models import user
from src.classes.authorization import Authorization
from .repository import AbstractRepository


class UserRepository(AbstractRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def get_user_by_email(self, email: str) -> user.Profile | None:
        query = sqlalchemy.select(user.Profile).filter(
            user.Profile.email == email
        )
        return self.session.execute(query).scalar()

    def create_user(
        self, email: str, password: str, name: str, photo: str | None = None
    ) -> None:
        hashed_password = Authorization().get_hashed_password(password)
        query = sqlalchemy.insert(user.Profile).values(
            email=email, password=hashed_password, name=name, photo=photo
        )
        self.session.execute(query)
        self.session.commit()
