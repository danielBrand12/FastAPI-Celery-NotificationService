from tortoise import fields, models


class Cart(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="user_cart")
    product = fields.ForeignKeyField("models.Product", related_name="product_cart")
    quantity = fields.IntField()
    created_at = fields.DatetimeField(auto_now_add=True)
    last_modified = fields.DatetimeField(auto_now=True)
