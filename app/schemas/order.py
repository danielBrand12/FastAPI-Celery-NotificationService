from datetime import datetime
from pydantic import BaseModel
from enum import Enum


class OrderStatus(str, Enum):
    CREATED = "created"
    CONFIRMED = "confirmed"
    CANCELED = "canceled"


class Order(BaseModel):
    user_id: int
    created_by_id: int
    status: OrderStatus


class CreateOrder(Order):
    pass


class UpdateOrder(Order):
    pass


class OrderInDB(Order):
    id: int
    created_at: datetime | None = None
    last_modified: datetime | None = None
