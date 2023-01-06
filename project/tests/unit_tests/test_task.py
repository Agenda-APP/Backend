from fastapi import status
from sqlalchemy import exists, func

from src.database.models import Task


def test_create_task(client, session, created_category, daily_task):
    assert daily_task.status_code == status.HTTP_201_CREATED
    assert session.query(exists().where(Task.id == 1)).scalar()


def test_delete_task(client, session, created_category, daily_task):
    response = client.delete(url="api/task/1")
    assert response.status_code == status.HTTP_200_OK
    assert session.query(func.count(Task.description)).scalar() == 0


def test_update_task(client, session, created_category, daily_task):
    updated_task = {
        "status": "Создано",
        "end_date": "2022-12-27T12:10:03.500Z",
        "description": "Пойти в ресторан",
        "category": {"name": "Основные"},
        "priority": "Срочно сделать",
    }
    response = client.put("/api/task/1", json=updated_task)
    assert response.status_code == status.HTTP_200_OK
    assert session.query(
        exists().where(Task.description == updated_task.get("description"))
    ).scalar()
