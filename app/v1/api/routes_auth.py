from fastapi import APIRouter, Depends

from app.core.jwt import create_access_token
from app.core.logging_config import logger
from app.crud.user_crud import create_user, authenticate_user, activate_user, reset_user_password
from app.crud.user_crud import get_current_user
from app.db.models.user import User
from app.schemas.user import UserCreate, UserOut
from app.utils.enum import ResultCodes
from app.utils.utils import success_response, error_response
from app.v1.deps import get_db

router = APIRouter()

# oath2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/login')

@router.get('/check-login/')
async def get_items(user=Depends(get_current_user)):
    return {
        "token": 'authenticated',
        "user": user.username,
    }


@router.get('/get_profile/', response_model=UserOut)
async def get_profile(db=Depends(get_db), user=Depends(get_current_user)):
    profile = db.query(User).filter(User.username == user.username).first()
    if profile:
        return profile
    else:
        return error_response(result=ResultCodes.USER_NOT_FOUND, message={'detail': 'User not found'})


@router.post('/login/')
async def login(username: str, password: str, db=Depends(get_db)):
    auth_user = authenticate_user(db, username, password)

    if not auth_user:
        return error_response(result=ResultCodes.INVALID_CREDENTIALS, message={'detail': 'Invalid username or password'})
    if auth_user.is_active == False:
        activate_user(db, username)

    token = create_access_token(data={"sub": auth_user.username})
    return {"token_type": "bearer", "access_token": token}


@router.post('/register/', response_model=UserOut)
async def register(user: UserCreate, db=Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        return error_response(result=ResultCodes.USER_ALREADY_EXISTS, message={"detail": "User already exists"})
    try:
        user_in = create_user(db, username=user.username,
                              email=user.email, name=user.name,
                              password=user.password)
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        return error_response(result=ResultCodes.FAIL, message={"detail": str(e)})
    response = UserOut(
        id=user_in.id,
        username=user_in.username,
        email=user_in.email,
        is_active=user_in.is_active,
        is_verified=user_in.is_verified
    )
    return success_response(data=response.dict(), status_code=201)


@router.get('/get-all-users/', response_model=list[UserOut])
async def get_all_users(db=Depends(get_db)):
    users = db.query(User).all()
    users = [UserOut.from_orm(u).model_dump() for u in users]
    return success_response(data=users)


@router.get('/reset-password/', response_model=UserOut, dependencies=[Depends(get_current_user)])
async def reset_password(username: str, new_password: str, db=Depends(get_db)):
    user = reset_user_password(db, username, new_password)
    # response = UserOut(user)
    if user:
        return user
    else:
        return error_response(result=ResultCodes.USER_NOT_FOUND, message={'detail': 'User not found'})
