import logging
from sqlalchemy.orm import Session

from app import crud, schemas
from app.db import base  # noqa: F401
from app.core.config import settings

logger = logging.getLogger(__name__)


BOOKS = [
    {
        "id": 1,
        "title": "Man and the Lion",
        "description": "This is a story about a man and a lion",
        "cover_image": "http://www.manandthelion.com/images/logo.png",
        "price": 39.3,
    }
]


# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)
    if settings.FIRST_SUPERUSER:
        user = crud.user.get_by_username(db, username=settings.FIRST_SUPERUSER)
        if not user:
            user_in = schemas.UserCreate(
                first_name="Super",
                last_name="Admin",
                username=settings.FIRST_SUPERUSER,
                author_pseudonym="Super Admin",
                is_superuser=True,
                password=settings.FIRST_SUPERUSER_PW,
            )
            user = crud.user.create(db, obj_in=user_in)  # noqa: F841
        else:
            logger.warning(
                "Skipping creating superuser. User with username "
                f"{settings.FIRST_SUPERUSER} already exists. "
            )
        if not user.books:
            for book in BOOKS:
                book_in = schemas.BookCreate(
                    title=book["title"],
                    description=book["description"],
                    cover_image=book["cover_image"],
                    price=book["price"],
                    author_id=user.id,
                )
                crud.book.create(db, obj_in=book_in)
    else:
        logger.warning(
            "Skipping creating superuser.  FIRST_SUPERUSER needs to be "
            "provided as an env variable. "
            "e.g.  FIRST_SUPERUSER=admin@wookiebooks.com"
        )
