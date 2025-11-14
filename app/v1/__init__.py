from fastapi import APIRouter
from .api import routes_test, routes_post, routes_auth

router = APIRouter()
router.include_router(routes_test.router, prefix="/test", tags=["Test Routes"])
router.include_router(routes_post.router, prefix="/posts", tags=["Post Routes"])
router.include_router(routes_auth.router, prefix="/auth", tags=["Auth Routes"])