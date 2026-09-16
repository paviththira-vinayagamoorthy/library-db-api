from datetime import date
from typing import TYPE_CHECKING
from sqlalchemy import String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.connection import Base

if TYPE_CHECKING:
    from app.models.member import Member
    from app.models.book import Book

class Borrow(Base):
    __tablename__ = "borrows"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"), nullable=False)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), nullable=False)
    
    borrow_date: Mapped[date] = mapped_column(Date, nullable=False)
    due_date: Mapped[date] = mapped_column(Date, nullable=False)
    return_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="Borrowed")  # Borrowed, Returned, Overdue

    # Relationships
    member: Mapped["Member"] = relationship("Member", back_populates="borrows")
    book: Mapped["Book"] = relationship("Book", back_populates="borrows")