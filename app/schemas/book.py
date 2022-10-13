from pydantic import BaseModel, HttpUrl

from typing import Sequence, Optional

from app.schemas.user import User


class BookBase(BaseModel):
    title: str
    description: str
    price: float
    cover_image: HttpUrl


class BookCreate(BookBase):
    title: str
    description: str
    price: float
    cover_image: HttpUrl


class BookUpdate(BookBase):
    id: int
    title: str
    description: str
    price: float
    cover_image: HttpUrl


class BookUpdateRestricted(BaseModel):
    id: int
    title: str
    description: str
    price: float
    cover_image: HttpUrl

class BookDelete(BaseModel):
    id: int


# Properties shared by models stored in DB
class BookInDBBase(BookBase):
    id: int
    author_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Book(BookInDBBase):
    id: int
    author: Optional[User] = None


# Properties properties stored in DB
class BookInDB(BookInDBBase):
    pass


class BookWithAuthor(BookInDBBase):
    author: Optional[User] = None


class BookSearchResults(BaseModel):
    results: Sequence[BookWithAuthor]
