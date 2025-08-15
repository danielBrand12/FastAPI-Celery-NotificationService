from app.db.models.product import Product
from app.schemas.product import CreateProduct, UpdateProduct
from app.service.base_service import BaseService

class ProductService(BaseService[Product, CreateProduct, UpdateProduct]):
    def __init__(self, model):
        super().__init__(model)

product_service = ProductService(model=Product)
