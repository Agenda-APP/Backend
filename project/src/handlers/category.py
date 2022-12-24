from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from database.dependency import get_database_session
from database.repositories.category import CategoryRepository
from src.errors.existence import AlreadyExistsError
from src.schemas.category import CategoryCreation, CategoryDeletion
from src.services.category import CategoryService


router = APIRouter(prefix="/category", tags=["category"])


@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_category(
    category: CategoryCreation,
    session: Session = Depends(get_database_session),
):
    try:
        CategoryService(CategoryRepository(session)).create_new_category(
            category=category.name
        )
    except AlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category already exists",
        )
    return {"message": "Category has been created"}


@router.delete("/delete", status_code=status.HTTP_200_OK)
def delete_category(
    category: CategoryDeletion,
    session: Session = Depends(get_database_session),
):
    CategoryService(CategoryRepository(session)).delete_existing_category(
        category=category.name
    )
    return {"message": "Category has been deleted"}
