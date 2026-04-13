from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship
from .basemodel import BaseModel

class User(BaseModel):
    __tablename__ = 'users'

    username = Column(String)
    name = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    posts = relationship('Post', back_populates='user')
