from app.db.models.role import Role
from app.schemas.role import CreateRole, UpdateRole
from app.service.base_service import BaseService

class RoleService(BaseService[Role, CreateRole, UpdateRole]):
    def __init__(self, model):
        super().__init__(model)

role_service = RoleService(model=Role)
