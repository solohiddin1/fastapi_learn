from app.db.models.user import User
from sqlalchemy.orm import Session
from app.core.security import hash_password, verify_password

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