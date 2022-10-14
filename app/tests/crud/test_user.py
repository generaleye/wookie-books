from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud
from app.core.security import verify_password
from app.core.auth import authenticate
from app.schemas.user import UserCreate, UserUpdate
from app.tests.utils.utils import random_email, random_lower_string


def test_create_user(db: Session) -> None:
    first_name = random_lower_string()
    last_name = random_lower_string()
    author_pseudonym = random_lower_string()
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(first_name=first_name, last_name=last_name, author_pseudonym=author_pseudonym,
                         username=username, password=password)
    user = crud.user.create(db, obj_in=user_in)
    assert user.first_name == first_name
    assert user.last_name == last_name
    assert user.author_pseudonym == author_pseudonym
    assert user.username == username
    assert hasattr(user, "hashed_password")


def test_authenticate_user(db: Session) -> None:
    first_name = random_lower_string()
    last_name = random_lower_string()
    author_pseudonym = random_lower_string()
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(first_name=first_name, last_name=last_name, author_pseudonym=author_pseudonym,
                         username=username, password=password)
    user = crud.user.create(db, obj_in=user_in)
    authenticated_user = authenticate(db=db, username=username, password=password)
    assert authenticated_user
    assert user.username == authenticated_user.username


def test_not_authenticate_user(db: Session) -> None:
    username = random_email()
    password = random_lower_string()
    user = authenticate(db=db, username=username, password=password)
    assert user is None


def test_get_user(db: Session) -> None:
    first_name = random_lower_string()
    last_name = random_lower_string()
    author_pseudonym = random_lower_string()
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(first_name=first_name, last_name=last_name, author_pseudonym=author_pseudonym,
                         username=username, password=password)
    user = crud.user.create(db, obj_in=user_in)
    user_2 = crud.user.get(db, id=user.id)
    assert user_2
    assert user.username == user_2.username
    assert jsonable_encoder(user) == jsonable_encoder(user_2)


def test_update_user(db: Session) -> None:
    first_name = random_lower_string()
    last_name = random_lower_string()
    author_pseudonym = random_lower_string()
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(first_name=first_name, last_name=last_name, author_pseudonym=author_pseudonym,
                         username=username, password=password)
    user = crud.user.create(db, obj_in=user_in)
    new_pseudonym = random_lower_string()
    user_in_update = UserUpdate(id=user.id, author_pseudonym=new_pseudonym)
    crud.user.update(db, db_obj=user, obj_in=user_in_update)
    user_2 = crud.user.get(db, id=user.id)
    assert user_2
    assert user.username == user_2.username
    assert user.author_pseudonym == user_2.author_pseudonym
