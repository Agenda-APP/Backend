from fastapi import APIRouter, Depends, status

from src.business_logic import providers
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
    category_service.create_new_category(category=category.name)
    return {"message": "Category has been created", **category.dict()}


@router.delete("/delete/{category_id}", status_code=status.HTTP_200_OK)
def delete_category(
    category_id: int,
    category_service: CategoryService = Depends(
        providers.category_service_provider
    ),
):
    category_service.delete_existing_category(category_id=category_id)
    return {"message": "Category has been deleted"}
