from fastapi import status
from sqlalchemy import exists, func

from database.models.task import Task


def test_create_task(client, session, daily_task):
    assert daily_task.status_code == status.HTTP_201_CREATED
    assert session.query(exists().where(Task.id == 1)).scalar()


def test_delete_task(client, session, daily_task, token):
    response = client.delete(url="api/task/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_200_OK
    assert session.query(func.count(Task.description)).scalar() == 0


def test_update_task(client, session, daily_task, token):
    updated_task = {
        "user_id": 1,
        "status": "Создано",
        "end_date": "2022-12-27T12:10:03.500Z",
        "description": "Пойти в ресторан",
        "category": "Основные",
        "priority": "Срочно сделать",
    }
    response = client.put("/api/task/1", json=updated_task, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_200_OK
    assert session.query(
        exists().where(Task.description == updated_task.get("description"))
    ).scalar()


def test_get_active_tasks_being_authorized(
    client, daily_task, token
):
    response = client.get(
        "/api/tasks/active/1", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1


def test_get_active_tasks_being_unauthorized(client, daily_task):
    response = client.get(
        "/api/tasks/active/1",
        headers={"Authorization": "Bearer non-existent-token"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Invalid token" in response.json()["detail"]


def test_get_done_tasks_being_authorized(client, done_task, token):
    response = client.get(
        "/api/tasks/done/1", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1


def test_get_done_tasks_being_unauthorized(client, daily_task):
    response = client.get(
        "/api/tasks/done/1",
        headers={"Authorization": "Bearer non-existent-token"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Invalid token" in response.json()["detail"]
