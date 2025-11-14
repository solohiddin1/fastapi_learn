from fastapi import APIRouter, Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from app.schemas.user import UserCreate

router = APIRouter()

oath2_scheme = OAuth2PasswordBearer(tokenUrl='token')

@router.get('/items/')
async def get_items(token: Annotated[str, Depends(oath2_scheme)]):
    return {"token": token}

@router.post('/create_user/')
async def register_user(user: UserCreate):
    return {"username": user.username, "name": user.name, "email": user.email}