from fastapi import APIRouter
from app.api.product import router as product_router
from app.api.auth import router as auth_router
from app.api.view import router as view_router
main_router = APIRouter()
main_router.include_router(product_router, tags=['product'])
main_router.include_router(auth_router, tags=['auth'])
main_router.include_router(view_router, tags=['view'])


