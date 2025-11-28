from fastapi import APIRouter, Depends

from app.core.logging_config import logger
from app.crud.post_crud import create_post, show_posts, \
                            show_post_detail, show_my_posts, \
                            update_post
from app.crud.user_crud import get_current_user
from app.v1.deps import get_db
from app.db.models.post import Post
from app.db.models.user import User
from app.utils import success_response, error_response
from app.schemas.posts import PostCreate, PostOut

from sqlalchemy.orm import Session

router = APIRouter(
    prefix='',
    # tags=['posts'],
    dependencies=[Depends(get_current_user)]
)

@router.get('/posts_list/')
async def get_posts(db=Depends(get_db)):
    logger.info("get posts is called")
    posts = show_posts(db)
    return success_response(posts)


@router.get('/my_posts/')
async def my_posts(db=Depends(get_db),
                      current_user=Depends(get_current_user)
                      ):
    logger.info("my posts is called")
    post = show_my_posts(db=db, user_id=current_user.id)
    return success_response(post)
    

@router.get('/post_detail/')
async def post_detail(id: int, 
                      db=Depends(get_db)
                      ):
    logger.info("post detail is called")
    post = show_post_detail(id=id, db=db)
    return success_response(post)
    

@router.patch('/post_update/')
async def post_update(id: int, 
                      data:PostCreate,
                      db=Depends(get_db),
                      current_user=Depends(get_current_user)
                      ):
    logger.info(f"update post is called")
    post = update_post(id=id, data=data, 
                       db=db, 
                       current_user=current_user)
    if not post:
        return error_response(data='post not found!', status_code=404)
    if post:
        return success_response(PostOut.model_validate(post).model_dump())
    
    return None


@router.post('/post_create/')
async def post_create(post: PostCreate,  
                      db: Session = Depends(get_db),
                      current_user: User=(Depends(get_current_user))
                      ):

    post_in = create_post(db=db, 
                          title=post.title, 
                          text=post.text,
                          user_id=current_user.id
                          )
    return success_response(PostOut.from_orm(post_in).model_dump())
