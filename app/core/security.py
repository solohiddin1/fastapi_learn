from passlib.context import CryptContext

pwd_passlib = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash_password(plain: str):
    return pwd_passlib.hash(plain)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_passlib.verify(plain_password, hashed_password)