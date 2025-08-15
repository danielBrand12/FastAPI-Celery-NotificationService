from app.db.models.user import User
from app.schemas.user import CreateUser, UpdateUser
from app.service.base_service import BaseService

class UserService(BaseService[User, CreateUser, UpdateUser]):
    async def get_by_username(self, username: str):
        return await self.model.get_or_none(username=username)

    async def get_by_email(self, email: str):
        return await self.model.get_or_none(email=email)

user_service = UserService(model=User)
