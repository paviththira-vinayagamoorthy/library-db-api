from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate, BookResponse, StockUpdate

router = APIRouter(
    prefix="/books",
    tags=["Books"]
)

# Get books with search, filters, sorting & pagination
@router.get("/", response_model=list[BookResponse])
def get_books(
    category_id: int | None = None,
    author_id: int | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    available: bool | None = None,
    search: str | None = None,
    sort_by: str | None = Query(None, pattern="^(price|title)$"),
    order: str | None = Query("asc", pattern="^(asc|desc)$"),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(Book)

    if category_id:
        query = query.filter(Book.category_id == category_id)
    if author_id:
        query = query.filter(Book.author_id == author_id)
    if min_price is not None:
        query = query.filter(Book.price >= min_price)
    if max_price is not None:
        query = query.filter(Book.price <= max_price)
    if available is not None:
        query = query.filter(Book.available == available)
    if search:
        query = query.filter(Book.title.ilike(f"%{search}%"))

    if sort_by:
        col = getattr(Book, sort_by)
        query = query.order_by(col.desc() if order == "desc" else col.asc())

    offset = (page - 1) * limit
    return query.offset(offset).limit(limit).all()

# Get book by ID
@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# Create book
@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    new_book = Book(
        title=book.title,
        price=book.price,
        stock=book.stock,
        available=book.stock > 0,
        author_id=book.author_id,
        category_id=book.category_id
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

# Update book details
@router.put("/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book_update: BookUpdate, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    update_data = book_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(book, key, value)

    book.available = book.stock > 0
    db.commit()
    db.refresh(book)
    return book

# Stock Management endpoint
@router.patch("/{book_id}/stock", response_model=BookResponse)
def update_stock(book_id: int, stock_data: StockUpdate, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    book.stock = stock_data.stock
    book.available = book.stock > 0
    db.commit()
    db.refresh(book)
    return book

# Delete book
@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(book)
    db.commit()
    return {"message": "Book deleted successfully"}