import sqlalchemy
from sqlalchemy.orm import Session

from database.models import task
from .repository import AbstractRepository


class CategoryRepository(AbstractRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def create_category(self, name) -> None:
        query = sqlalchemy.insert(task.Category).values(name=name)
        self.session.execute(query)
        self.session.commit()

    def get_id_of_category(self, name: str) -> int | None:
        query = sqlalchemy.select(task.Category.id).filter(
            task.Category.name == name
        )
        return self.session.execute(query).scalar()

    def delete_category(self, category: str) -> None:
        self.session.execute(
            sqlalchemy.delete(task.Category).where(
                task.Category.name == category
            )
        )
        self.session.commit()
