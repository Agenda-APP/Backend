from fastapi import APIRouter, Depends, status

from application import providers, dependencies
from application.schemas.category import CategoryCreation
from application.services.category import CategoryService


router = APIRouter(tags=["category"])


@router.post(
    "/api/category",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(dependencies.check_auth())],
)
def create_category(
    category: CategoryCreation,
    category_service: CategoryService = Depends(
        providers.category_service_provider
    ),
):
    category_id = category_service.create_new_category(category=category.name)
    return {
        "message": "Category has been created",
        "id": category_id,
        **category.dict(),
    }


@router.delete(
    "/api/category/{category_id}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(dependencies.check_auth())],
)
def delete_category(
    category_id: int,
    category_service: CategoryService = Depends(
        providers.category_service_provider
    ),
):
    category_service.delete_existing_category(category_id=category_id)
    return {"message": "Category has been deleted"}
