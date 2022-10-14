from typing import Optional

from sqlalchemy.orm import Session

from app import crud, models
from app.schemas.book import Book, BookCreate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string, random_price, random_url


def create_random_book(db: Session, *, author_id: Optional[int] = None) -> Book:
    if author_id is None:
        user = create_random_user(db)
        author_id = user.id
    title = random_lower_string()
    description = random_lower_string()
    price = random_price()
    cover_image = random_url()
    book_in = BookCreate(title=title, description=description, price=price, cover_image=cover_image, id=id)
    return crud.book.create_with_author(db=db, obj_in=book_in, author_id=author_id)
