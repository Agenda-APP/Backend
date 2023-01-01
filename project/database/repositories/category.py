import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy.sql import exists

from database.models import task
from src.dto.task import CategoryDTO
from .repository import AbstractRepository


class CategoryRepository(AbstractRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def create_category(self, name: str) -> None:
        query = sqlalchemy.insert(task.Category).values(name=name)
        self.session.execute(query)
        self.session.commit()

    def get_id_of_category(self, name: str | CategoryDTO) -> int | None:
        query = sqlalchemy.select(task.Category.id).where(
            task.Category.name == name
        )
        return self.session.execute(query).scalar()

    def delete_category(self, category_id: int) -> None:
        self.session.execute(
            sqlalchemy.delete(task.Category).where(
                task.Category.id == category_id
            )
        )
        self.session.commit()

    def is_exist(self, category_id: int) -> bool:
        return self.session.query(
            exists().where(task.Category.id == category_id)
        ).scalar()
