from app.db.base import Base
from app.db.session import engine

from app.db.models.user import User
from app.db.models.post import Post

from app.core.logging_config import logger

Base.metadata.create_all(bind=engine)

logger.info("Tables created successfully!")
print("Tables created successfully!")