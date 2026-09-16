from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Database மற்றும் Models
from app.database.connection import engine, Base
import app.models

# Routers Import
from app.routers.authors import router as author_router
from app.routers.categories import router as category_router
from app.routers.books import router as book_router
from app.routers.members import router as member_router
from app.routers.borrows import router as borrow_router
from app.routers.stats import router as stat_router

# Table Creation in MySQL
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Library Management API"
)

# React CORS Permission
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React app address
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include All Routers
app.include_router(author_router)
app.include_router(category_router)
app.include_router(book_router)
app.include_router(member_router)
app.include_router(borrow_router)
app.include_router(stat_router)

@app.get("/")
def home():
    return {
        "message": "Library Management API is running successfully!"
    }