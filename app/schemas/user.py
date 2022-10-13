from typing import Optional, Sequence

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[EmailStr] = None
    author_pseudonym: Optional[str] = None
    is_superuser: bool = False


# Properties to receive via API on creation
class UserCreate(UserBase):
    username: EmailStr
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    id: int


class UserDelete(BaseModel):
    id: int


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties stored in DB but not returned by API
class UserInDB(UserInDBBase):
    hashed_password: str


# Additional properties to return via API
class User(UserInDBBase):
    pass


class UserAuthor(BaseModel):
    author_pseudonym: str


class UserSearchResults(BaseModel):
    results: Sequence[User]