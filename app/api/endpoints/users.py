from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from app.schemas.user import CreateUser, UserInDB
from app.service.user_service import user_service
from app.security import get_password_hash

router = APIRouter()

@router.post(
    "",
    response_class=JSONResponse,
    response_model=UserInDB,
    status_code=201,
    responses={
        201: {"description": "User created."},
        400: {"description": "Username or email already exists"},
    },
)
async def create_user(user_in: CreateUser) -> UserInDB:
    existing_user = await user_service.get_by_username(user_in.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    existing_email = await user_service.get_by_email(user_in.email)
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user_in.password)
    
    user_data = user_in.model_dump()
    user_data["password"] = hashed_password
    
    user_to_create = CreateUser(**user_data)
    
    new_user = await user_service.create(user_to_create)

    return new_user
