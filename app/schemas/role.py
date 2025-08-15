from datetime import datetime
from pydantic import BaseModel, Json


class Role(BaseModel):
    name: str
    description: str | None = None
    scopes: Json | None = None


class CreateRole(Role):
    pass


class UpdateRole(Role):
    pass

class RoleInDB(Role):
    id: int
    created_at: datetime | None = None
    last_modified: datetime | None = None
