from datetime import datetime
from pydantic import BaseModel


class Cart(BaseModel):
    user_id: int
    product_id: int
    quantity: int


class CreateCart(Cart):
    pass


class UpdateCart(Cart):
    pass


class CartInDB(Cart):
    id: int
    created_at: datetime | None = None
    last_modified: datetime | None = None
 

class PayloadCart(BaseModel):
    user_id: int | None = None
    product_id: int | None = None
    quantity: int | None = None
