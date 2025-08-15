from fastapi import APIRouter
from .endpoints.users import router as users_router
from .endpoints.product import router as product_router
from .endpoints.cart import router as cart_router
from .endpoints.order import router as order_router

api_router = APIRouter()

api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(product_router, prefix="/products", tags=["products"])
api_router.include_router(cart_router, prefix="/carts", tags=["carts"])
api_router.include_router(order_router, prefix="/orders", tags=["orders"])
