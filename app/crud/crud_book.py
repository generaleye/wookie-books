from typing import Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.book import Book
from app.models.user import User
from app.schemas.book import BookCreate, BookUpdateRestricted, BookUpdate


class CRUDBook(CRUDBase[Book, BookCreate, BookUpdate]):
    def create_with_author(
        self, db: Session, *, obj_in: BookCreate, author_id: int
    ) -> Book:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, author_id=author_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: User,
        obj_in: Union[BookUpdate, BookUpdateRestricted]
    ) -> Book:
        db_obj = super().update(db, db_obj=db_obj, obj_in=obj_in)
        return db_obj


book = CRUDBook(Book)
