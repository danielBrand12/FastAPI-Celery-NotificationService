from typing_extensions import Annotated

from fastapi import APIRouter, Response, Security
from fastapi.responses import JSONResponse

from app.service.cart_service import cart_service
from app.schemas.cart import CreateCart, CartInDB
from app.schemas.user import User
from app.security import get_current_active_user

router = APIRouter()


@router.post(
    "",
    response_class=JSONResponse,
    response_model=CartInDB,
    status_code=201,
    responses={
        201: {"description": "Cart created."},
        400: {"description": "Bad request"},
    },
)
async def create(
    *, 
    current_user: Annotated[User, Security(get_current_active_user, scopes=["create"])],
    cart_in: CreateCart
) -> CartInDB:
    cart = await cart_service.create(cart_in)
    return cart


@router.delete(
    "/{user_id}/items/{product_id}",
    response_class=Response,
    status_code=200,
    responses={
        200: {"description": "Cart item deleted."},
        400: {"description": "Bad request"},
    },
)
async def delete_item(
    *,
    current_user: Annotated[User, Security(get_current_active_user, scopes=["delete"])],
    user_id: int,
    product_id: int
) -> Response:
    cart = await cart_service.delete_item(user_id, product_id)
    status = 204 if cart == 1 else 404
    return Response(status_code=status)
