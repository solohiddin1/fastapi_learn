from pydantic import BaseModel, Field
from typing import Annotated, Optional
from .user import UserOut


class PostCreate(BaseModel):
    title: Annotated[str, Field(min_length=1, max_length=100)]
    text: Annotated[str, Field()]


class PostOut(BaseModel):
    title: str
    text: str
    user_id: Optional[int] = None
    user : Optional[UserOut] = None

    class Config:
        from_attributes = True
