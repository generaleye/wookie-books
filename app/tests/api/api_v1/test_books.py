from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.book import create_random_book


def test_create_book(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    data = {"title": "Return of the Jedi", "description": "Story about the return of the Jedi",
            "price": 49.0, "cover_image": "http://returnofthejedi.com/logo.png"}
    response = client.post(
        f"{settings.API_V1_STR}/books/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 201
    content = response.json()
    assert content["title"] == data["title"]
    assert content["description"] == data["description"]
    # assert content["price"] == data["price"]
    assert content["cover_image"] == data["cover_image"]
    assert "id" in content
    assert "author_id" in content


def test_read_book(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    book = create_random_book(db)
    response = client.get(
        f"{settings.API_V1_STR}/books/{book.id}", headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == book.title
    assert content["description"] == book.description
    # assert content["price"] == book.price
    assert content["cover_image"] == book.cover_image
    assert content["id"] == book.id
    assert content["author_id"] == book.author_id
