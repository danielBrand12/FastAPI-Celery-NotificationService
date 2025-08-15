from tortoise import fields, models


class User(models.Model):
    id = fields.IntField(pk=True)
    role = fields.ForeignKeyField("models.Role", related_name="users")
    name = fields.CharField(max_length=255)
    username = fields.CharField(max_length=255)
    password = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255, unique=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    last_modified = fields.DatetimeField(auto_now=True)