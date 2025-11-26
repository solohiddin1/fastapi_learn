from datetime import datetime, timedelta
from jose import jwt
from app.core.config import settings

def create_access_token(data: dict, expire_delta: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=expire_delta)
    to_encode.update({'exp':expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
