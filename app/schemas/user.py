from datetime import datetime
from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field
)


class UserRegister(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=50
    )

    email: EmailStr

    full_name: str = Field(
        min_length=2,
        max_length=100
    )

    password: str = Field(
        min_length=8,
        max_length=128
    )

    # Postman-ல் role அனுப்பினால் அதை எடுக்கும், இல்லையென்றால் default-ஆக "member" எனச் சேமிக்கும்
    role: str = Field(default="member")


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: str
    role: str
    active: bool
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None