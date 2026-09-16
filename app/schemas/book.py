from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class BookCreate(BaseModel):
    title: str = Field(min_length=2)
    price: float = Field(gt=0)
    stock: int = Field(ge=0)
    author_id: int
    category_id: int

class BookUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=2)
    price: Optional[float] = Field(default=None, gt=0)
    stock: Optional[int] = Field(default=None, ge=0)
    author_id: Optional[int] = None
    category_id: Optional[int] = None

class StockUpdate(BaseModel):
    stock: int = Field(ge=0)

class BookResponse(BaseModel):
    id: int
    title: str
    price: float
    stock: int
    available: bool
    author_id: int
    category_id: int

    model_config = ConfigDict(from_attributes=True)