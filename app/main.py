import redis
from fastapi import FastAPI
from fastapi_admin.app import app as admin_app
from app.v1 import router as v1_router
from app.core.logging_config import logger
from app.core.config import settings
from app.middleware.middleware import ProcessTimeMiddleware
from fastapi.middleware.cors import CORSMiddleware
from examples.models import Admin
from fastapi_admin.providers.login import UsernamePasswordProvider
from sqladmin import Admin as SQLAdmin, ModelView
from app.db.session import engine
from app.db.models.user import User

app = FastAPI(title=settings.APP_NAME, version="1.0.0")

@app.get('/', include_in_schema=False)
async def get_home():
    logger.info('backend is running')
    return {"message":"Backend is running!"}


login_provider = UsernamePasswordProvider(
    admin_model=Admin,
    # enable_captcha=True,
    login_logo_url="https://preview.tabler.io/static/logo.svg"
)

# @app.on_event("startup")
# async def startup():
#     redis = await redis.create_redis_pool("redis://localhost", encoding="utf8")
#     admin_app.configure(
#         logo_url="https://preview.tabler.io/static/logo-white.svg",
#         template_folders=[os.path.join(BASE_DIR, "templates")],
#         providers=[login_provider],
#         redis=redis,
#     )

origins = [
    "https://fastapi-admin-pro.long2ice.io",
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

    await admin_app.configure(
        redis=redis_conn,
        providers=[login_provider],
        logo_url="https://preview.tabler.io/static/logo-white.svg",
    )

admin = SQLAdmin(app, engine)

class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username]


app.mount("/admin", admin_app)
app.add_middleware(ProcessTimeMiddleware)
admin.add_view(UserAdmin)
app.include_router(v1_router, prefix='/api/v1')