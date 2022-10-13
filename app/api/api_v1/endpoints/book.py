import asyncio
from typing import Any, Optional

import httpx
from fastapi import APIRouter, Depends, HTTPException, Query
# from fastapi_pagination import paginate, Page, Params
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.schemas.book import (
    Book,
    BookCreate,
    BookUpdate,
    BookSearchResults,
    BookUpdateRestricted,
    BookDelete
)
from app.models.user import User

router = APIRouter()


@router.get("/", status_code=200, response_model=BookSearchResults)
def all_books(
    *,
    limit: Optional[int] = 10,
    page: Optional[int] = 0,
    db: Session = Depends(deps.get_db),
) -> dict:
    """
    Return all books
    """
    books = crud.book.get_multi(db=db, skip=page, limit=limit)

    return {"results": list(books)}


@router.get("/{book_id}", status_code=200, response_model=Book)
def single_book(
    *,
    book_id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Fetch a single book by ID
    """
    result = crud.book.get(db=db, id=book_id)
    if not result:
        # the exception is raised, not returned - you will get a validation
        # error otherwise.
        raise HTTPException(
            status_code=404, detail=f"Book with ID {book_id} not found"
        )

    return result


@router.get("/mine/", status_code=200, response_model=BookSearchResults)
def fetch_user_books(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Fetch all books for a user
    """
    books = current_user.books

    if not books:
        return {"results": list()}

    return {"results": list(books)}


@router.post("/", status_code=201, response_model=Book)
def create_book(
    *,
    book_in: BookCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> dict:
    """
    Create a new book in the database.
    """

    print(current_user.first_name)
    if (current_user.first_name == 'Darth' and current_user.last_name == 'Vader') \
            or (current_user.author_pseudonym == 'Darth Vader'):
        raise HTTPException(
            status_code=403, detail=f"You can not publish your books."
        )

    book = crud.book.create_with_author(db=db, obj_in=book_in, author_id=current_user.id)

    return book


@router.put("/", status_code=200, response_model=Book)
def update_book(
    *,
    book_in: BookUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> dict:
    """
    Update book in the database.
    """
    book = crud.book.get(db, id=book_in.id)
    if not book:
        raise HTTPException(
            status_code=400, detail=f"Book with ID: {book_in.id} not found."
        )

    if book.author_id != current_user.id:
        raise HTTPException(
            status_code=403, detail=f"You can only update your books."
        )

    updated_book = crud.book.update(db=db, db_obj=book, obj_in=book_in)
    return updated_book


@router.delete("/", status_code=200)
def unpublish_book(
    *,
    book_in: BookDelete,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> dict:
    """
    Update book in the database.
    """
    book = crud.book.get(db, id=book_in.id)
    if not book:
        raise HTTPException(
            status_code=400, detail=f"Book with ID: {book_in.id} not found."
        )

    if book.author_id != current_user.id:
        raise HTTPException(
            status_code=403, detail=f"You can only delete your books."
        )

    deleted_book = crud.book.remove(db=db, id=book.id)
    return {"status": "success", "message": "Book has been deleted successfully"}
