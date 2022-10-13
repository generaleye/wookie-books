from sqlalchemy import Integer, String, Column, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(256), nullable=True)
    last_name = Column(String(256), nullable=True)
    username = Column(String, index=True, nullable=False)
    author_pseudonym = Column(String(256), nullable=False)
    is_superuser = Column(Boolean, default=False)
    books = relationship(
        "Book",
        cascade="all,delete-orphan",
        back_populates="author",
        uselist=True,
    )

    # New addition
    hashed_password = Column(String, nullable=False)
