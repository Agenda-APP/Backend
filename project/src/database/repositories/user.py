import sqlalchemy
from sqlalchemy.orm import Session

from src.database.models import user
from src.business_logic.classes.authentication import Authentication
from .repository import AbstractRepository


class UserRepository(AbstractRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def get_user_by_email(self, email: str) -> user.Profile | None:
        query = sqlalchemy.select(user.Profile).where(
            user.Profile.email == email
        )
        return self.session.execute(query).scalar()

    def create_user(
        self,
        email: str,
        password: str,
        name: str | None,
        photo: str | None = None,
    ) -> None:
        hashed_password = Authentication().get_hashed_password(password)
        query = sqlalchemy.insert(user.Profile).values(
            email=email, password=hashed_password, name=name, photo=photo
        )
        self.session.execute(query)
        self.session.commit()
