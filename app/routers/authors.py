from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.author import Author
from app.schemas.author import AuthorCreate, AuthorUpdate, AuthorResponse
from app.schemas.book import BookResponse

router = APIRouter(
    prefix="/authors",
    tags=["Authors"]
)

# Get all authors
@router.get("/", response_model=list[AuthorResponse])
def get_authors(db: Session = Depends(get_db)):
    return db.query(Author).all()

# Get author by ID
@router.get("/{author_id}", response_model=AuthorResponse)
def get_author(author_id: int, db: Session = Depends(get_db)):
    author = db.query(Author).filter(Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author

# Get all books by an author
@router.get("/{author_id}/books", response_model=list[BookResponse])
def get_author_books(author_id: int, db: Session = Depends(get_db)):
    author = db.query(Author).filter(Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author.books

# Create author
@router.post("/", response_model=AuthorResponse, status_code=status.HTTP_201_CREATED)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    if db.query(Author).filter(Author.email == author.email).first():
        raise HTTPException(status_code=400, detail="Author with this email already exists")

    new_author = Author(
        name=author.name,
        email=author.email,
        country=author.country
    )
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author

# Update author
@router.put("/{author_id}", response_model=AuthorResponse)
def update_author(author_id: int, author_update: AuthorUpdate, db: Session = Depends(get_db)):
    author = db.query(Author).filter(Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    update_data = author_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(author, key, value)

    db.commit()
    db.refresh(author)
    return author

# Delete author
@router.delete("/{author_id}")
def delete_author(author_id: int, db: Session = Depends(get_db)):
    author = db.query(Author).filter(Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    db.delete(author)
    db.commit()
    return {"message": "Author deleted successfully"}