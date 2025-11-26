from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials

from app.db.models.user import User
from app.schemas.user import UserCreate, UserOut
from app.v1.deps import get_db
from app.crud.user_crud import create_user, authenticate_user
from app.core.jwt import create_access_token
from app.core.logging_config import logger
from app.crud.user_crud import get_current_user

router = APIRouter()


# oath2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/login')

@router.get('/check/')
async def get_items(user = Depends(get_current_user)):
    return {
        "token": 'You are authenticated', 
        # "user": user
            }

@router.get('/get_profile/')
async def get_profile(db = Depends(get_db), user=Depends(get_current_user)):
    print(user)
    profile = db.query(User).filter(User.username == user[0]).first()
    # profile = db.query(User).all()
    if profile:
        return profile
    else:
        return Response(status_code=400, content={'detail': 'User not found'})

@router.post('/login/')
async def login(username: str, password: str, db = Depends(get_db)):
    auth_user = authenticate_user(db, username, password)
    if not auth_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token(data={"sub": auth_user.username})
    return {"token": token, "token_type": "bearer"}


@router.post('/create_user/')
async def register_user(user: UserCreate, db = Depends(get_db)):
    userin = User(
        username = user.username,
        name = user.name,
        email = user.email,
        password = user.password
    )
    return {"username": user.username, "name": user.name, "email": user.email}


@router.post('/register/', response_model=UserOut)
async def register(user: UserCreate, db = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    try:
        user_in = create_user(db, username=user.username, email=user.email, name=user.name, password=user.password)
    except Exception as e:
        logger.info(f"Error creating user: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    response = UserOut(
        id=user_in.id,
        username=user_in.username,
        email=user_in.email,
    )
    return response
