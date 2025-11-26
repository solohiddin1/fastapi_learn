from sqlalchemy.orm import Session

from app.core.logging_config import logger
from app.core.config import settings
from jose import jwt, ExpiredSignatureError
from app.db.models.user import User
from app.core.security import hash_password, verify_password

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException

security = HTTPBearer()

def create_user(db: Session, username: str, email: str, name: str, password: str):
    userin = User(
        username=username,
        name=name,
        email=email,
        hashed_password=hash_password(password)
    )
    db.add(userin)
    db.commit()
    db.refresh(userin)
    return userin

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """it was put here cause in one api it was 
    not seeing token so i turned off auto error in router, 
    now its useless"""
    # if not credentials:
    #     raise HTTPException(status_code=401, detail='No token was provided')
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user = payload.get("sub")
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid token credentials")
    except ExpiredSignatureError:
        logger.error("Token has expired")
        raise HTTPException(status_code=401, detail="Token has expired")
    except Exception as e:
        logger.error(f"Token decoding error: {e}")
        raise HTTPException(status_code=401, detail="Invalid token credentials")
    
    return token
