from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.schemas.user import UserCreate
from app.tests.utils.utils import random_email, random_lower_string


def test_create_user_new_username(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    first_name = random_lower_string()
    last_name = random_lower_string()
    author_pseudonym = random_lower_string()
    username = random_email()
    password = random_lower_string()
    data = {
        "first_name": first_name,
        "last_name": last_name,
        "username": username,
        "author_pseudonym": author_pseudonym,
        "password": password
    }
    r = client.post(
        f"{settings.API_V1_STR}/users/", headers=superuser_token_headers, json=data,
    )
    assert 200 <= r.status_code < 300
    created_user = r.json()
    user = crud.user.get_by_username(db, username=username)
    assert user
    assert user.username == created_user["username"]


def test_get_existing_user(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    first_name = random_lower_string()
    last_name = random_lower_string()
    author_pseudonym = random_lower_string()
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(first_name=first_name, last_name=last_name, author_pseudonym=author_pseudonym,
                         username=username, password=password)
    user = crud.user.create(db, obj_in=user_in)
    user_id = user.id
    r = client.get(
        f"{settings.API_V1_STR}/users/{user_id}", headers=superuser_token_headers,
    )
    assert 200 <= r.status_code < 300
    api_user = r.json()
    existing_user = crud.user.get_by_username(db, username=username)
    assert existing_user
    assert existing_user.username == api_user["username"]


def test_retrieve_users(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    first_name = random_lower_string()
    last_name = random_lower_string()
    author_pseudonym = random_lower_string()
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(first_name=first_name, last_name=last_name, author_pseudonym=author_pseudonym,
                         username=username, password=password)
    crud.user.create(db, obj_in=user_in)

    first_name2 = random_lower_string()
    last_name2 = random_lower_string()
    author_pseudonym2 = random_lower_string()
    username2 = random_email()
    password2 = random_lower_string()
    user_in2 = UserCreate(first_name=first_name2, last_name=last_name2, author_pseudonym=author_pseudonym2,
                         username=username2, password=password2)
    crud.user.create(db, obj_in=user_in2)

    r = client.get(f"{settings.API_V1_STR}/users/", headers=superuser_token_headers)
    all_users = r.json()

    assert len(all_users['results']) > 1
    for user in all_users['results']:
        assert "username" in user
