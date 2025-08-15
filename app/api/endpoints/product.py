from typing import Any, Optional

from fastapi import APIRouter, Depends, Security 
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.schemas.product import CreateProduct, ProductInDB
from app.security import get_current_active_user
from app.schemas.user import User
from app.service.product_service import product_service
from typing_extensions import Annotated

router = APIRouter()

class PayloadProduct(BaseModel):
    name: Optional[str] = None

@router.get(
    "",
    response_class=JSONResponse,
    response_model=list[ProductInDB] | None,
    status_code=200,
    responses={
        200: {"description": "Product found."},
        404: {"description": "Product not found"},
    },
)
async def get_all(
    *,
    product_in: PayloadProduct = Depends(PayloadProduct),
    skip: int = 0,
    limit: int = 100,
    current_user: Annotated[User, Security(get_current_active_user, scopes=["read"])],
) -> list[dict[str, Any] | None]:
    products = await product_service.get_all(filters=product_in.model_dump(exclude_none=True), skip=skip, limit=limit)
    return products


@router.post(
    "",
    response_class=JSONResponse,
    response_model=ProductInDB,
    status_code=201,
    responses={
        201: {"description": "Product created."},
        400: {"description": "Bad request"},
        403: {"description": "Forbidden"},
    },
)
async def create(
    *,
    product_in: CreateProduct,
    current_user: Annotated[User, Security(get_current_active_user, scopes=["create:product"])],
) -> ProductInDB:
    product = await product_service.create(product_in)
    return product

