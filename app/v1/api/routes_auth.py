from fastapi import APIRouter, Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from app.db.models.user import User
from app.schemas.user import UserCreate
from app.v1.deps import get_db
from app.crud.user_crud import create_user, authenticate_user

router = APIRouter()

oath2_scheme = OAuth2PasswordBearer(tokenUrl='token')

@router.get('/items/')
async def get_items(token: Annotated[str, Depends(oath2_scheme)]):
    return {"token": token}

@router.post('/create_user/')
async def register_user(user: UserCreate, db = Depends(get_db)):
    userin = User(
        username = user.username,
        name = user.name,
        email = user.email
    )
    return {"username": user.username, "name": user.name, "email": user.email}