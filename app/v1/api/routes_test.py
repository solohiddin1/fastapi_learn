from fastapi import APIRouter, Depends, Query, Header
from typing import Optional, Annotated

from app.core.logging_config import logger
from app.v1.deps import get_db

from app.db.models.user import User
from app.schemas.user import UserCreate

router = APIRouter()

@router.get("/hello_world/")
async def hello_world(db = Depends(get_db)):
    logger.info("hello world endpoint was called")
    return db.query(User).all()
    # return 'Hello world!'

# @router.post('/add_user')
# async def add_user(user: UserCreate, db = Depends(get_db)):
#     logger.info(f"Creating user {user.name}")
#     print(user)
#     db_user = User(
#         name = user.name,
#         email = user.email
#     )
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return user.name


# @router.get("/test/")
# async def test_endpoint(name : Optional[str] = None):
#     logger.info(f"test endpoint was called with name: {name}")
#     return {"message": f"Test endpoint received name: {name}"}


# @router.get("/test2/")
# async def test_endpoint(limit : Annotated[int, Query(gt=0, le=100)] = None):
#     logger.info(f"test2 endpoint was called with limit: {limit}")
#     return {"message": f"Test2 endpoint received limit: {limit}"}


# @router.get("/test3/")
# async def test_endpoint(limit : int = Query(... ,gt=0, le=100)):
#     logger.info(f"test3 endpoint was called with limit: {limit}")
#     return {"message": f"Test3 endpoint received limit: {limit}"}


# @router.get("/test4/")
# async def test_endpoint(limit : Annotated[int, Header()]):
#     logger.info(f"test4 endpoint was called with limit: {limit}")
#     return {"message": f"Test4 endpoint received limit: {limit}"}