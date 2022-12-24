from fastapi import status
from sqlalchemy import exists, func

from database.models.task import Category


def test_create_category(client, session):
    category = {"name": "Основные"}
    response = client.post(url="/category/create", json=category)
    assert response.status_code == status.HTTP_201_CREATED
    assert session.query(exists().where(Category.name == "Основные")).scalar()


def test_delete_category(client, session):
    category = {"name": "Основные"}
    client.post(url="/category/create", json=category)
    response = client.delete(url="/category/delete", json=category)
    assert response.status_code == status.HTTP_200_OK
    assert session.query(func.count(Category.name)).scalar() == 0
