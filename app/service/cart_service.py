from app.db.models.cart import Cart
from app.schemas.cart import CreateCart, UpdateCart
from app.service.base_service import BaseService

class CartService(BaseService[Cart, CreateCart, UpdateCart]):
    def __init__(self, model):
        super().__init__(model)

    async def upsert_item(self, user_id: int, product_id: int, quantity: int) -> Cart:
        cart_item = await self.model.get_or_none(user_id=user_id, product_id=product_id)
        if cart_item:
            cart_item.quantity = quantity
            await cart_item.save()
            return cart_item
        else:
            return await self.create(CreateCart(user_id=user_id, product_id=product_id, quantity=quantity))

    async def delete_item(self, user_id: int, product_id: int) -> int:
        return await self.model.filter(user_id=user_id, product_id=product_id).delete()

cart_service = CartService(model=Cart)
