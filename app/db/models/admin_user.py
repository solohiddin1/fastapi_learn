from fastapi_admin.models import AbstractAdmin
from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship


class AdminUser(AbstractAdmin):
    __tablename__ = 'admin_users'

    username = Column(String)
    name = Column(String)
    email = Column(String)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    posts = relationship('Post', back_populates='user')
