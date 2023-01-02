from fastapi import status
from sqlalchemy import exists, func

from database.models.task import Category


def test_create_category(client, session, created_category):
    assert created_category.status_code == status.HTTP_201_CREATED
    assert session.query(exists().where(Category.name == "Основные")).scalar()


def test_delete_category(client, session, created_category):
    response = client.delete(url="api/category/delete/1")
    assert response.status_code == status.HTTP_200_OK
    assert session.query(func.count(Category.name)).scalar() == 0
