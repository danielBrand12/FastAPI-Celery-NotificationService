from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class Product(BaseModel):
    name: str
    description: str | None = None
    price: float
    stock: int


class CreateProduct(Product):
    pass


class UpdateProduct(Product):
    pass


class ProductInDB(Product):
    id: int
    created_at: datetime | None = None
    last_modified: datetime | None = None


class PayloadProduct(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
