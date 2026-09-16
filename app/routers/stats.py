from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.author import Author
from app.models.book import Book
from app.models.borrow import Borrow
from app.models.category import Category
from app.models.member import Member

router = APIRouter(
    prefix="/stats",
    tags=["Statistics"]
)

# 1. Basic Library Statistics
@router.get("/summary")
def get_library_summary(db: Session = Depends(get_db)):
    total_books = db.query(Book).count()
    total_stock_quantity = db.query(func.sum(Book.stock)).scalar() or 0
    total_authors = db.query(Author).count()
    total_categories = db.query(Category).count()
    total_members = db.query(Member).count()
    
    available_books = db.query(Book).filter(Book.available == True).count()
    unavailable_books = db.query(Book).filter(Book.available == False).count()
    
    currently_borrowed_books = db.query(Borrow).filter(Borrow.status == "Borrowed").count()
    returned_books = db.query(Borrow).filter(Borrow.status == "Returned").count()
    overdue_books = db.query(Borrow).filter(Borrow.status == "Overdue").count()

    return {
        "total_books": total_books,
        "total_stock_quantity": total_stock_quantity,
        "total_authors": total_authors,
        "total_categories": total_categories,
        "total_members": total_members,
        "available_books": available_books,
        "unavailable_books": unavailable_books,
        "currently_borrowed_books": currently_borrowed_books,
        "returned_books": returned_books,
        "overdue_books": overdue_books,
    }


# 2. Advanced Statistics & Analytics
@router.get("/advanced")
def get_advanced_stats(db: Session = Depends(get_db)):
    # 1. Most borrowed books
    most_borrowed = (
        db.query(Book.id, Book.title, func.count(Borrow.id).label("borrow_count"))
        .join(Borrow, Book.id == Borrow.book_id)
        .group_by(Book.id)
        .order_by(func.count(Borrow.id).desc())
        .limit(5)
        .all()
    )

    # 2. Top members who borrowed the most books
    top_members = (
        db.query(Member.id, Member.name, func.count(Borrow.id).label("borrow_count"))
        .join(Borrow, Member.id == Borrow.member_id)
        .group_by(Member.id)
        .order_by(func.count(Borrow.id).desc())
        .limit(5)
        .all()
    )

    # 3. Number of books in each category
    books_per_category = (
        db.query(Category.name, func.count(Book.id).label("book_count"))
        .outerjoin(Book, Category.id == Book.category_id)
        .group_by(Category.id)
        .all()
    )

    return {
        "most_borrowed_books": [
            {"id": book_id, "title": title, "borrow_count": count}
            for book_id, title, count in most_borrowed
        ],
        "top_members": [
            {"id": member_id, "name": name, "borrow_count": count}
            for member_id, name, count in top_members
        ],
        "category_distribution": [
            {"category": category_name, "book_count": count}
            for category_name, count in books_per_category
        ],
    }