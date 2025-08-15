from typing import Type, TypeVar, Generic, Any, Optional
from pydantic import BaseModel
from tortoise.models import Model

ModelType = TypeVar("ModelType", bound=Model)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get_all(self, filters: Optional[dict] = None, skip: int = 0, limit: int = 100) -> list[ModelType]:
        query = self.model.all()
        if filters:
            query = query.filter(**filters)
        return await query.offset(skip).limit(limit)

    async def get_by_id(self, obj_id: Any) -> Optional[ModelType]:
        return await self.model.get_or_none(id=obj_id)

    async def create(self, obj_in: CreateSchemaType) -> ModelType:
        obj = await self.model.create(**obj_in.model_dump())
        return obj

    async def update(self, obj_id: Any, obj_in: UpdateSchemaType) -> Optional[ModelType]:
        updated_count = await self.model.filter(id=obj_id).update(**obj_in.model_dump(exclude_unset=True))
        if updated_count:
            return await self.model.get(id=obj_id)
        return None

    async def delete(self, obj_id: Any) -> int:
        return await self.model.filter(id=obj_id).delete()
