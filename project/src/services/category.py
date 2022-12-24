import sqlalchemy.exc
from database.repositories.category import CategoryRepository
from src.errors import existence


class CategoryService:
    def __init__(self, category_repository: CategoryRepository):
        self.category_repository = category_repository

    def create_new_category(self, category: str) -> None:
        try:
            self.category_repository.create_category(name=category)
        except sqlalchemy.exc.IntegrityError:
            raise existence.AlreadyExistsError

    def delete_existing_category(self, category: str) -> None:
        self.category_repository.delete_category(category=category)
