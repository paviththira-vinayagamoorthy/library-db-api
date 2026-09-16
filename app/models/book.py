from typing import List, TYPE_CHECKING
from sqlalchemy import String, Float, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.connection import Base

if TYPE_CHECKING:
    from app.models.author import Author
    from app.models.category import Category
    from app.models.borrow import Borrow

class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    stock: Mapped[int] = mapped_column(default=0)
    available: Mapped[bool] = mapped_column(Boolean, default=True)

    # Foreign Keys
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)

    # Relationships
    author_rel: Mapped["Author"] = relationship("Author", back_populates="books")
    category_rel: Mapped["Category"] = relationship("Category", back_populates="books")
    borrows: Mapped[List["Borrow"]] = relationship("Borrow", back_populates="book")