from datetime import datetime
from pydantic import BaseModel


class User(BaseModel):
    name: str
    username: str
    email: str
    role_id: int
    created_at: datetime | None = None
    last_modified: datetime | None = None


class CreateUser(BaseModel):
    name: str
    username: str
    email: str
    role_id: int
    password: str


class CreateDefaultUser(BaseModel):
    id: int
    name: str
    username: str
    email: str
    role_id: int
    password: str


class UpdateUser(BaseModel):
    username: str | None = None
    email: str | None = None
    role_id: int | None = None
    password: str | None = None
    last_modified: datetime | None = None


class UserInDB(User):
    id: int
