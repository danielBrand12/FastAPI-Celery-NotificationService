from tortoise import fields, models
from app.schemas.order import OrderStatus


class Order(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="user_orders")
    created_by = fields.ForeignKeyField("models.User", related_name="created_by_orders", null=True)
    status = fields.CharEnumField(max_length=50, enum_type=OrderStatus, default=OrderStatus.CREATED)
    created_at = fields.DatetimeField(auto_now_add=True)
    last_modified = fields.DatetimeField(auto_now=True)