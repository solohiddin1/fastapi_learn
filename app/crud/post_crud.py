from app.db.models.post import Post
from sqlalchemy.orm import Session
from app.schemas.posts import PostOut, PostOutDetail
from fastapi import Depends
from app.v1.deps import get_db
from app.db.models.user import User
from app.utils import error_response


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
        return PostOutDetail.from_orm(post).model_dump(mode="json")
    else:
        return None

def update_post(id: int, data:dict = None, db=Session, current_user:int=None):
    post = db.query(Post).filter(Post.id == id, Post.user_id==current_user.id).first()

    if not post:
        return None
    if post.user_id is None:
        return error_response(data='post does not belong to you', status_code=400)
    if post.user_id != current_user.id or current_user.is_superuser:
        raise error_response(data='You can update posts only that belong to you',status_code=401)
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(post, key, value)
    
    db.commit()
    db.refresh(post)
    
    return post
    # return PostOut.from_orm(post)
