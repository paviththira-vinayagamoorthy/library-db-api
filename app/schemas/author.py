from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Optional

class AuthorCreate(BaseModel):
    name: str = Field(min_length=2)
    email: EmailStr
    country: Optional[str] = None

class AuthorUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2)
    email: Optional[EmailStr] = None
    country: Optional[str] = None

class AuthorResponse(BaseModel):
    id: int
    name: str
    email: str
    country: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)