from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date

class BorrowCreate(BaseModel):
    member_id: int
    book_id: int
    due_date: date

class BorrowResponse(BaseModel):
    id: int
    member_id: int
    book_id: int
    borrow_date: date
    due_date: date
    return_date: Optional[date] = None
    status: str

    model_config = ConfigDict(from_attributes=True)