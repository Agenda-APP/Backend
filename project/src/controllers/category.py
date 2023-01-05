from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

from src.business_logic import providers
from src.business_logic.errors import existence
from src.business_logic.schemas.category import CategoryCreation
from src.business_logic.services.category import CategoryService


router = APIRouter(prefix="/api/category", tags=["category"])


@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_category(
    category: CategoryCreation,
    category_service: CategoryService = Depends(
        providers.category_service_provider
    ),
):
    try:
        category_service.create_new_category(category=category.name)
    except existence.AlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category already exists",
        )
    return {"message": "Category has been created", **category.dict()}


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
