from tortoise.contrib.fastapi import register_tortoise
from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.exceptions import IntegrityError
from app.db.models import user, role, product
from app.security import get_password_hash
from app.core.settings import settings


def gen_config(models: str) -> dict:
    return {
        "connections": {
            "default": {
                "engine": "tortoise.backends.asyncpg",
                "credentials": {
                    "database": settings.POSTGRES_DB,
                    "host": settings.POSTGRES_HOST,
                    "password": settings.POSTGRES_PASSWORD,
                    "port": settings.POSTGRES_PORT,
                    "user": settings.POSTGRES_USER,
                    "minsize": settings.POSTGRES_MINSIZE,
                    "maxsize": settings.POSTGRES_MAXSIZE,
                },
            },
        },
        "apps": {"models": {"models": [models], "default_connection": "default"}},
    }

async def register_orm(app: FastAPI) -> None:
    register_tortoise(
        app,
        config=gen_config('app.db.models'),
        generate_schemas=False,
        add_exception_handlers=True
    )
    await Tortoise.init(
        config=gen_config('app.db.models'),
        modules={"models": ["db.models"]}
    )

    await Tortoise.generate_schemas()

    if settings.CREATE_DEFAULT_DATA:
        await create_default_roles()
        await create_default_products()


async def create_default_roles() -> None:
    roles_list = [
        {
            'id': 1,
            'name': 'ADMIN',
            'description': 'Administrator with full access',
            'scopes': ['create', 'read', 'update', 'delete', 'me', 'create:product', 'update:user']
        },
        {
            'id': 2,
            'name': 'CLIENT',
            'description': 'Client with read access',
            'scopes': ['create', 'read', 'update', 'delete', 'me']
        },
        {
            'id': 3,
            'name': 'ADVISOR',
            'description': 'Advisor with read and update access',
            'scopes': ['create', 'read', 'update', 'delete', 'me']
        },
    ]

    print("Creating default roles...")
    print('-'*20)

    for role_data in roles_list:
        print(f"Creating role: {role_data['name']}...")
        try:
            obj = await role.Role.create(**role_data)
            await obj.save()
        except IntegrityError as e:
            print(f"Role {role_data['name']} already exists. Skipping creation.")
            continue


async def create_default_products() -> None:
    products_list = [
        {
            'id': 1,
            'name': 'Product A',
            'description': 'Description for Product A',
            'price': 10.99,
            'stock': 100
        },
        {
            'id': 2,
            'name': 'Product B',
            'description': 'Description for Product B',
            'price': 15.49,
            'stock': 150
        },
        {
            'id': 3,
            'name': 'Product C',
            'description': 'Description for Product C',
            'price': 7.99,
            'stock': 200
        },
        {
            'id': 4,
            'name': 'Product D',
            'description': 'Description for Product D',
            'price': 12.49,
            'stock': 120
        },
        {
            'id': 5,
            'name': 'Product E',
            'description': 'Description for Product E',
            'price': 9.99,
            'stock': 80
        },
    ]

    print("Creating default products...")
    print('-'*20)

    for product_data in products_list:
        print(f"Creating product: {product_data['name']}...")
        try:
            obj = await product.Product.create(**product_data)
            await obj.save()
        except IntegrityError as e:
            print(f"Product {product_data['name']} already exists. Skipping creation.")
            continue
