from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.borrow import Borrow
from app.models.member import Member
from app.models.book import Book
from app.schemas.borrow import BorrowCreate, BorrowResponse

router = APIRouter(
    prefix="/borrows",
    tags=["Borrowing Operations"]
)

# Borrow a book
@router.post("/borrow", response_model=BorrowResponse, status_code=status.HTTP_201_CREATED)
def borrow_book(borrow_data: BorrowCreate, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.id == borrow_data.member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    if not member.active:
        raise HTTPException(status_code=400, detail="Member account is inactive")

    book = db.query(Book).filter(Book.id == borrow_data.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if book.stock <= 0:
        raise HTTPException(status_code=400, detail="Book is out of stock")

    new_borrow = Borrow(
        member_id=borrow_data.member_id,
        book_id=borrow_data.book_id,
        borrow_date=date.today(),
        due_date=borrow_data.due_date,
        status="Borrowed"
    )

    book.stock -= 1
    if book.stock == 0:
        book.available = False

    db.add(new_borrow)
    db.commit()
    db.refresh(new_borrow)
    return new_borrow

# Return a book
@router.post("/return/{borrow_id}", response_model=BorrowResponse)
def return_book(borrow_id: int, db: Session = Depends(get_db)):
    borrow = db.query(Borrow).filter(Borrow.id == borrow_id).first()
    if not borrow:
        raise HTTPException(status_code=404, detail="Borrow record not found")
    if borrow.status == "Returned":
        raise HTTPException(status_code=400, detail="Book has already been returned")

    borrow.return_date = date.today()
    borrow.status = "Returned"

    book = db.query(Book).filter(Book.id == borrow.book_id).first()
    if book:
        book.stock += 1
        book.available = True

    db.commit()
    db.refresh(borrow)
    return borrow

# Get borrow history for a specific book
@router.get("/book/{book_id}", response_model=list[BorrowResponse])
def get_book_borrow_history(book_id: int, db: Session = Depends(get_db)):
    return db.query(Borrow).filter(Borrow.book_id == book_id).all()

# Get all overdue books
@router.get("/overdue", response_model=list[BorrowResponse])
def get_overdue_books(db: Session = Depends(get_db)):
    today = date.today()
    return db.query(Borrow).filter(Borrow.due_date < today, Borrow.status == "Borrowed").all()