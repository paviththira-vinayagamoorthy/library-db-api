from fastapi import FastAPI
from app.database.connection import engine, Base  # அல்லது app.database.database

# Models
from app.models.author import Author
from app.models.category import Category
from app.models.book import Book
from app.models.member import Member
from app.models.borrow import Borrow
from app.models.user import User  # app. சேர்த்துள்ளோம்

# Routers
from app.routers.authors import router as authors_router
from app.routers.categories import router as categories_router
from app.routers.books import router as books_router
from app.routers.members import router as members_router
from app.routers.borrows import router as borrows_router
from app.routers.stats import router as stats_router
from app.routers.auth import router as auth_router  # app. சேர்த்துள்ளோம்

# Create Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Library Management API",
    version="1.0.0"
)

# Include Routers
app.include_router(auth_router)
app.include_router(authors_router)
app.include_router(categories_router)
app.include_router(books_router)
app.include_router(members_router)
app.include_router(borrows_router)
app.include_router(stats_router)