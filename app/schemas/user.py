from pydantic import BaseModel, EmailStr, validator, Field
from app.core.logging_config import logger
from typing import Annotated

class UserCreate(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=20)]
    name: Annotated[str, Field(min_length=3, max_length=10)]
    email: EmailStr
    # is_active: bool = False
    # is_superuser: bool = False

    @validator('name')
    def name_must_not_be_short(cls, v):
        if len(v) < 3:
            logger.error("Name too short attempted")
            raise ValueError("The name must be at least 3 characters long.")
        return v
    
    @validator('email')
    def validate_email(cls, v):
        if not v.endswith(('.com', '.ru')):
            logger.error(f"Invalid email domain attempted: {v}")
            raise ValueError("Registration using '@example.com' email addresses is not allowed.")
        return v
    
class UserRead(BaseModel):
    id: int
    username: str
    name: str
    email: EmailStr
    is_active: bool
    is_superuser: bool

    class Config:
        orm_mode = True
