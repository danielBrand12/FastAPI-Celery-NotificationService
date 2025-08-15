from fastapi import HTTPException
from tortoise import transactions
from app.db.models.order import Order, OrderStatus
from app.db.models.order_product import OrderProduct
from app.db.models.product import Product
from app.schemas.order import CreateOrder, UpdateOrder
from app.service.base_service import BaseService
from app.service.cart_service import cart_service

class OrderService(BaseService[Order, CreateOrder, UpdateOrder]):
    def __init__(self, model):
        super().__init__(model)

    async def create_from_cart(self, user_id: int, created_by_id: int) -> Order:
        async with transactions.in_transaction():
            cart_items = await cart_service.get_all(filters={"user_id": user_id})
            if not cart_items:
                raise HTTPException(status_code=400, detail="Cart is empty")

            order = await self.create(CreateOrder(user_id=user_id, created_by_id=created_by_id, status=OrderStatus.CREATED))

            for item in cart_items:
                await OrderProduct.create(
                    order_id=order.id,
                    product_id=item.product_id,
                    quantity=item.quantity
                )
            
            await cart_service.model.filter(user_id=user_id).delete()

            return order

    async def confirm_order(self, order_id: int) -> Order:
        async with transactions.in_transaction():
            order = await self.get_by_id(order_id)
            if not order:
                raise HTTPException(status_code=404, detail="Order not found")
            if order.status != OrderStatus.CREATED:
                raise HTTPException(status_code=400, detail="Order is not in created state")

            order_products = await OrderProduct.filter(order_id=order.id)
            for op in order_products:
                product = await Product.get(id=op.product_id)
                if product.stock < op.quantity:
                    raise HTTPException(status_code=400, detail=f"Not enough stock for product {product.name}")
                product.stock -= op.quantity
                await product.save()
            
            order.status = OrderStatus.CONFIRMED
            await order.save()
            return order

    async def cancel_order(self, order_id: int) -> Order:
        async with transactions.in_transaction():
            order = await self.get_by_id(order_id)
            if not order:
                raise HTTPException(status_code=404, detail="Order not found")

            if order.status == OrderStatus.CONFIRMED:
                order_products = await OrderProduct.filter(order_id=order.id)
                for op in order_products:
                    product = await Product.get(id=op.product_id)
                    product.stock += op.quantity
                    await product.save()

            order.status = OrderStatus.CANCELED
            await order.save()
            return order

order_service = OrderService(model=Order)
