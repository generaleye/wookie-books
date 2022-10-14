import asyncio
from typing import Any, Optional

import httpx
from fastapi import APIRouter, Depends, HTTPException, Query
# from fastapi_pagination import paginate, Page, Params
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.schemas.user import (
    User,
    UserCreate,
    UserUpdate,
    UserSearchResults,
    UserDelete
)
from app.models.user import User as ModelsUser

router = APIRouter()


@router.get("/", status_code=200, response_model=UserSearchResults)
def all_users(
    *,
    limit: Optional[int] = 10,
    page: Optional[int] = 0,
    db: Session = Depends(deps.get_db),
    current_user: ModelsUser = Depends(deps.get_current_user),
) -> dict:
    """
    Return all users
    """
    users = crud.user.get_multi(db=db, skip=page, limit=limit)

    return {"results": list(users)}


@router.get("/{user_id}", status_code=200, response_model=User)
def single_user(
    *,
    user_id: int,
    db: Session = Depends(deps.get_db),
    current_user: ModelsUser = Depends(deps.get_current_user),
) -> Any:
    """
    Fetch a single user by ID
    """
    result = crud.user.get(db=db, id=user_id)
    if not result:
        # the exception is raised, not returned - you will get a validation
        # error otherwise.
        raise HTTPException(
            status_code=404, detail=f"User with ID {user_id} not found"
        )

    return result


@router.post("/", status_code=201, response_model=User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserCreate,
    current_user: ModelsUser = Depends(deps.get_current_user),
) -> Any:
    """
    Create new user.
    """

    user = db.query(ModelsUser).filter(ModelsUser.username == user_in.username).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    user = crud.user.create(db=db, obj_in=user_in)

    return user


@router.put("/", status_code=200, response_model=User)
def update_user(
    *,
    user_in: UserUpdate,
    db: Session = Depends(deps.get_db),
    current_user: ModelsUser = Depends(deps.get_current_user),
) -> dict:
    """
    Update user in the database.
    """
    user = crud.user.get(db, id=user_in.id)
    if not user:
        raise HTTPException(
            status_code=400, detail=f"User with ID: {user_in.id} not found."
        )

    updated_user = crud.user.update(db=db, db_obj=user, obj_in=user_in)
    return updated_user


@router.delete("/", status_code=200)
def delete_user(
    *,
    user_in: UserDelete,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> dict:
    """
    Update user in the database.
    """
    user = crud.user.get(db, id=user_in.id)
    if not user:
        raise HTTPException(
            status_code=400, detail=f"User with ID: {user_in.id} not found."
        )

    deleted_user = crud.user.remove(db=db, id=user.id)
    return {"status": "success", "message": "User has been deleted successfully"}
