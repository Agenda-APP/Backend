from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

from src import providers
from src.errors import existence
from src.errors.existence import AlreadyExistsError
from src.schemas.category import CategoryCreation
from src.services.category import CategoryService


router = APIRouter(prefix="/category", tags=["category"])


@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_category(
    category: CategoryCreation,
    category_service: CategoryService = Depends(
        providers.category_service_provider
    ),
):
    try:
        category_service.create_new_category(category=category.name)
    except AlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category already exists",
        )
    return {"message": "Category has been created"}


@router.delete("/delete/{category_id}", status_code=status.HTTP_200_OK)
def delete_category(
    category_id: int,
    category_service: CategoryService = Depends(
        providers.category_service_provider
    ),
):
    try:
        category_service.delete_existing_category(category_id=category_id)
    except existence.DoesNotExistError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category does not exist",
        )
    return {"message": "Category has been deleted"}
