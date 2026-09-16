from typing import List, TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.connection import Base

if TYPE_CHECKING:
    from app.models.book import Book

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # 1 Category -> Many Books Relationship
    books: Mapped[List["Book"]] = relationship("Book", back_populates="category_rel", cascade="all, delete-orphan")