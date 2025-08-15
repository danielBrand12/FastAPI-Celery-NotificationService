from datetime import datetime
from pydantic import BaseModel



class OrderProduct(BaseModel):
    order_id: int
    product_id: int
    quantity: int

class CreateOrderProduct(OrderProduct):
    pass


class UpdateOrderProduct(OrderProduct):
    pass


class OrderProductInDB(OrderProduct):
    id: int
    created_at: datetime | None = None
    last_modified: datetime | None = None 
