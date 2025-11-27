from app.db.session import SessionLocal
from app.db.models.user import User
from app.core.security import hash_password


db = SessionLocal()
existing_user = db.query(User).filter(User.username == 'admin').first()
if existing_user:
    print("Superuser 'admin' already exists.")
    exit()

superuser = User(
    username='admin',
    email='admin@gmail.com',
    name='Administrator',
    hashed_password=hash_password('adminpassword'),
    is_active=True,
    is_superuser=True,
    is_verified=True,
)
db.add(superuser)
db.commit()
db.refresh(superuser)
print("Superuser 'admin' created successfully.")