from fastapi import status
from sqlalchemy import exists, func

from database.models.task import Task


def test_create_task(client, session):
    client.post(url="/category/create", json={"name": "Еженедельные"})
    daily = {
        "description": "Пойти в магазин",
        "category": "Еженедельные",
        "status": "Создано",
        "priority": "Срочно сделать",
        "end_date": "2022-12-03T16:28:08.464Z",
    }
    response = client.post(url="/task/create", json=daily)
    assert response.status_code == status.HTTP_201_CREATED
    assert session.query(
        exists().where(Task.description == daily.get("description"))
    ).scalar()


def test_delete_task(client, session):
    task = {
        "description": "Убраться дома",
        "status": "Создано",
        "priority": "Необходимо сделать",
        "end_date": "2022-11-04T13:28:08.464Z",
    }
    client.post(url="/task/create", json=task)
    task_deletion_info = {"description": task.get("description")}
    response = client.delete(url="/task/delete", json=task_deletion_info)
    assert response.status_code == status.HTTP_200_OK
    assert session.query(func.count(Task.description)).scalar() == 0
