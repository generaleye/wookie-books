from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Book(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256), nullable=False)
    description = Column(String(256), nullable=False)
    cover_image = Column(String(256), index=True, nullable=True)
    price = Column(Numeric(10, 2), nullable=True)
    author_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    author = relationship("User", back_populates="books")