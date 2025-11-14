from fastapi import APIRouter
from app.core.logging_config import logger

router = APIRouter()

@router.get('/posts')
async def get_posts():
    logger.info("get posts is called")
    
    return {"post":"post"}