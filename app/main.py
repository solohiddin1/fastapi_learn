import redis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_admin.app import app as admin_app
from sqladmin import Admin as SQLAdmin

from app.admin.post import PostAdmin
from app.admin.user import UserAdmin
from app.core.config import settings
from app.core.logging_config import logger
from app.db.session import engine
from app.middleware.middleware import ProcessTimeMiddleware
from app.v1 import router as v1_router

app = FastAPI(title=settings.APP_NAME, version="1.0.0")


@app.get('/', include_in_schema=False)
async def get_home():
    logger.info('backend is running')
    return {"message": "Backend is running!"}


origins = [
    "http://localhost:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    redis_conn = redis.from_url(
        "redis://localhost",
        encoding="utf-8",
        decode_responses=True
    )


admin = SQLAdmin(app, engine)

app.mount("/admin", admin_app)
app.add_middleware(ProcessTimeMiddleware)
admin.add_view(UserAdmin)
admin.add_view(PostAdmin)
app.include_router(v1_router, prefix='/api/v1')
