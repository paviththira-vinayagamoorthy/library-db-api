from typing import List, TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.connection import Base

if TYPE_CHECKING:
    from app.models.book import Book

class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    country: Mapped[str | None] = mapped_column(String(50), nullable=True)

    # 1 Author -> Many Books Relationship
    books: Mapped[List["Book"]] = relationship("Book", back_populates="author_rel", cascade="all, delete-orphan")