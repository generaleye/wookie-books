from sqlalchemy.orm import Session

from app import crud
from app.schemas.book import BookCreate, BookUpdate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string, random_price, random_url


def test_create_book(db: Session) -> None:
    title = random_lower_string()
    description = random_lower_string()
    price = random_price()
    cover_image = random_url()
    book_in = BookCreate(title=title, description=description, price=price, cover_image=cover_image)
    user = create_random_user(db)
    book = crud.book.create_with_author(db=db, obj_in=book_in, author_id=user.id)
    assert book.title == title
    assert book.description == description
    # assert book.price == price
    assert book.cover_image == cover_image
    assert book.author_id == user.id


def test_get_book(db: Session) -> None:
    title = random_lower_string()
    description = random_lower_string()
    price = random_price()
    cover_image = random_url()
    book_in = BookCreate(title=title, description=description, price=price, cover_image=cover_image)
    user = create_random_user(db)
    book = crud.book.create_with_author(db=db, obj_in=book_in, author_id=user.id)
    stored_book = crud.book.get(db=db, id=book.id)
    assert stored_book
    assert book.id == stored_book.id
    assert book.title == stored_book.title
    assert book.description == stored_book.description
    # assert book.price == stored_book.price
    assert book.cover_image == stored_book.cover_image
    assert book.author_id == stored_book.author_id


def test_update_book(db: Session) -> None:
    title = random_lower_string()
    description = random_lower_string()
    price = random_price()
    cover_image = random_url()
    book_in = BookCreate(title=title, description=description, price=price, cover_image=cover_image)
    user = create_random_user(db)
    book = crud.book.create_with_author(db=db, obj_in=book_in, author_id=user.id)
    description2 = random_lower_string()
    book_update = BookUpdate(id=book.id, description=description2)
    book2 = crud.book.update(db=db, db_obj=book, obj_in=book_update)
    assert book.id == book2.id
    assert book.title == book2.title
    assert book2.description == description2
    # assert book.price == book2.price
    assert book.cover_image == book2.cover_image
    assert book.author_id == book2.author_id


def test_delete_book(db: Session) -> None:
    title = random_lower_string()
    description = random_lower_string()
    price = random_price()
    cover_image = random_url()
    book_in = BookCreate(title=title, description=description, price=price, cover_image=cover_image)
    user = create_random_user(db)
    book = crud.book.create_with_author(db=db, obj_in=book_in, author_id=user.id)
    book2 = crud.book.remove(db=db, id=book.id)
    book3 = crud.book.get(db=db, id=book.id)
    assert book3 is None
    assert book2.id == book.id
    assert book2.title == title
    assert book2.description == description
    # assert book2.price == price
    assert book2.cover_image == cover_image
    assert book2.author_id == user.id
