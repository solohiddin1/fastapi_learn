from sqlalchemy import Integer, Column, ForeignKey
from sqlalchemy.orm import relationship
from .basemodel import BaseModel

class Like(BaseModel):
    __tablename__='likes'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))
    user = relationship('User', back_populates='likes')