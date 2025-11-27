from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials

from app.db.models.user import User
from app.schemas.user import UserCreate, UserOut
from app.v1.deps import get_db
from app.crud.user_crud import create_user, authenticate_user, activate_user
from app.core.jwt import create_access_token
from app.core.logging_config import logger
from app.crud.user_crud import get_current_user
from app.utils import success_response
router = APIRouter()


# oath2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/login')

@router.get('/check/')
async def get_items(user = Depends(get_current_user)):
    return {
        "token": 'You are authenticated', 
        # "user": user
            }

@router.get('/get_profile/',response_model=UserOut)
async def get_profile(db = Depends(get_db), user=Depends(get_current_user)):
    profile = db.query(User).filter(User.username == user.username).first()
    if profile:
        return profile
    else:
        return Response(status_code=400, content={'detail': 'User not found'})


@router.post('/login/')
async def login(username: str, password: str, db = Depends(get_db)):
    auth_user = authenticate_user(db, username, password)

    if not auth_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    if auth_user.is_active == False:
        activate_user(db, username)

    token = create_access_token(data={"sub": auth_user.username})
    return {"token": token, "token_type": "bearer"}


@router.post('/register/', response_model=UserOut)
async def register(user: UserCreate, db = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    try:
        user_in = create_user(db, username=user.username, 
                              email=user.email, name=user.name, 
                              password=user.password)
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    response = UserOut(
        id=user_in.id,
        username=user_in.username,
        email=user_in.email,
        is_active=user_in.is_active,
        is_verified=user_in.is_verified
    )
    return success_response(data=response.dict(), status_code=201)