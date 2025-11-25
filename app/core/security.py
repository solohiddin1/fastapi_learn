from passlib.context import CryptContext
from app.core.logging_config import logger

pwd_passlib = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash_password(plain: str):
    b = plain.encode("utf-8")[:72]            # first 72 bytes
    logger.info(f"truncated password: {b}")
    truncated = b.decode("utf-8", errors="ignore")  # ignore partial char
    logger.info(f"truncated password: {truncated}")
    return pwd_passlib.hash(truncated)

def verify_password(plain_password: str, hashed_password: str):
    b = plain_password.encode("utf-8")[:72]            # first 72 bytes
    truncated = b.decode("utf-8", errors="ignore")  # ignore partial char
    return pwd_passlib.verify(truncated, hashed_password)