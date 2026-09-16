from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Optional
from datetime import datetime

class MemberCreate(BaseModel):
    name: str = Field(min_length=2)
    email: EmailStr
    phone: Optional[str] = None

class MemberUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    active: Optional[bool] = None

class MemberResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str] = None
    active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)