from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class CategoryCreate(BaseModel):
    name: str = Field(min_length=2)
    description: Optional[str] = None

class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2)
    description: Optional[str] = None

class CategoryResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)