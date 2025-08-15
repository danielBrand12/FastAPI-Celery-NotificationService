from typing import Annotated
from fastapi import APIRouter, Depends, Security, Security
from app.service.order_service import order_service
from app.schemas.order import OrderInDB
from app.schemas.user import User
from app.security import get_current_active_user

router = APIRouter()

@router.post("", response_model=OrderInDB)
async def create_order_from_cart(
    current_user: Annotated[User, Security(get_current_active_user, scopes=["create"])],
    user_id: int, 
    created_by: int | None = None, 
):
    return await order_service.create_from_cart(user_id, created_by)

@router.post("/{order_id}/confirm", response_model=OrderInDB)
async def confirm_order(
    order_id: int,
    current_user: Annotated[User, Security(get_current_active_user, scopes=["create"])]
):
    return await order_service.confirm_order(order_id)

@router.post("/{order_id}/cancel", response_model=OrderInDB)
async def cancel_order(
    order_id: int,
    current_user: Annotated[User, Security(get_current_active_user, scopes=["create"])]
    ):
    return await order_service.cancel_order(order_id)