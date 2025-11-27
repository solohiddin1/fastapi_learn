from app.db.models.post import Post
from sqlalchemy.orm import Session
from app.schemas.posts import PostOut
from fastapi import Depends
from app.v1.deps import get_db
from app.db.models.user import User


def create_post(db: Session, title: str=None, 
                text:str=None,
                user_id: int=None
                ):
    post = Post(
        title=title,
        text=text,
        user_id=user_id
    )
    db.add(post)
    db.commit()
    db.refresh(post)

    return post


def show_posts(db: Session):
    posts = db.query(Post).all()
    posts = [PostOut.from_orm(p).model_dump() for p in posts] # to show multiple posts
    
    return posts

def show_my_posts(db: Session, user_id: int):
    posts = db.query(Post).filter(Post.user_id==user_id)
    posts = [PostOut.from_orm(p).model_dump() for p in posts] # to show multiple posts
    
    return posts

def show_post_detail(id: int, db=Session):
    post = db.query(Post).filter(Post.id == id).first()
    if post:
        return PostOut.from_orm(post).model_dump()
    else:
        return None