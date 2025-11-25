from .basemodel import BaseModel
from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
# from .user import User

class Post(BaseModel):
    __tablename__ = 'posts'

    title = Column(String)
    text = Column(Text)
    user_id = Column(Integer,ForeignKey('users.id'))
    user = relationship('User', back_populates='posts')