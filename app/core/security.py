from passlib.context import CryptContext
from app.core.logging_config import logger

pwd_passlib = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash_password(plain: str):
    truncated_bytes = plain.encode("utf-8")[:72]            # first 72 bytes
    logger.info(f"truncated password: {truncated_bytes}")
    truncated = truncated_bytes.decode("utf-8", errors="ignore")  # ignore partial char
    logger.info(f"truncated password: {truncated}")
    return pwd_passlib.hash(truncated)

def verify_password(plain_password: str, hashed_password: str):
    truncated_bytes = plain_password.encode("utf-8")[:72]            # first 72 bytes
    truncated = truncated_bytes.decode("utf-8", errors="ignore")  # ignore partial char
    return pwd_passlib.verify(truncated, hashed_password)
