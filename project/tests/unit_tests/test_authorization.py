from fastapi import status
from sqlalchemy import exists

from src.database.models import Profile


def test_sign_up(client, session, photo):
    user = {"email": "test@mail.com", "password": "12345", "name": "Jim"}
    response = client.post(
        url="api/authorization/signup",
        data=user,
        files={"photo": ("photo.png", photo, "image/png")},
    )
    user_exists = session.query(
        exists().where(Profile.email == "test@mail.com")
    ).scalar()
    assert response.status_code == status.HTTP_201_CREATED
    assert user_exists


def test_sign_up_with_already_existent_email(client):
    user = {"email": "test@mail.com", "password": "12345", "name": "John"}
    client.post(url="api/authorization/signup", data=user)
    response = client.post(url="api/authorization/signup", data=user)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert len(response.json()) == 1
    assert "message" in response.json()


def test_login(client):
    user = {"email": "test@mail.com", "password": "12345", "name": "John"}
    client.post(url="api/authorization/signup", data=user)
    response = client.post(
        url="api/authorization/login",
        json={"email": "test@mail.com", "password": "12345"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert len(response.json()) == 3
    assert "access_token" in response.json()


def test_login_with_non_existent_email(client):
    user = {"email": "bob@mail.com", "password": "12345", "name": "Bob"}
    response = client.post(url="api/authorization/login", json=user)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "access_token" not in response.json()
