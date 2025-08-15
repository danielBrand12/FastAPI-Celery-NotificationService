from app.db.models.order_product import OrderProduct
from app.schemas.order_product import CreateOrderProduct, UpdateOrderProduct
from app.service.base_service import BaseService

class OrderProductService(BaseService[OrderProduct, CreateOrderProduct, UpdateOrderProduct]):
    def __init__(self, model):
        super().__init__(model)

order_product_service = OrderProductService(model=OrderProduct)
