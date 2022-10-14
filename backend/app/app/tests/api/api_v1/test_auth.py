from typing import Dict

from fastapi.testclient import TestClient

from app.core.config import settings
from app.tests.utils.utils import random_email, random_lower_string


def test_get_access_token(client: TestClient) -> None:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PW,
    }
    r = client.post(f"{settings.API_V1_STR}/auth/login", data=login_data)
    tokens = r.json()
    assert r.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]


def test_use_access_token(
    client: TestClient, superuser_token_headers: Dict[str, str]
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/auth/me", headers=superuser_token_headers,
    )
    result = r.json()
    assert r.status_code == 200
    assert "username" in result


def test_signup(client: TestClient) -> None:
    first_name = random_lower_string()
    last_name = random_lower_string()
    author_pseudonym = random_lower_string()
    username = random_email()
    password = random_lower_string()
    signup_data = {
        "first_name": first_name,
        "last_name": last_name,
        "username": username,
        "author_pseudonym": author_pseudonym,
        "password": password
    }
    r = client.post(f"{settings.API_V1_STR}/auth/signup", json=signup_data)
    result = r.json()
    assert r.status_code == 201
    assert "id" in result
