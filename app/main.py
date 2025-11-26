from fastapi import FastAPI
from fastapi_admin.app import app as admin_app
from app.v1 import router as v1_router
from app.core.logging_config import logger
from app.core.config import settings

app = FastAPI(title=settings.APP_NAME, version="1.0.0")
# logger.info("server started")
@app.get('/', include_in_schema=False)
async def get_home():
    logger.info('backend is running')
    return {"message":"Backend is running!"}

app.mount("/admin", admin_app)
app.include_router(v1_router, prefix='/api/v1')
