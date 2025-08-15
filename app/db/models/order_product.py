from tortoise import fields, models


class OrderProduct(models.Model):
    id = fields.IntField(pk=True)
    order = fields.ForeignKeyField("models.Order", related_name="order_products")
    product = fields.ForeignKeyField("models.Product", related_name="order_products")
    quantity = fields.IntField()
    created_at = fields.DatetimeField(auto_now_add=True)
    last_modified = fields.DatetimeField(auto_now=True)