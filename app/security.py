from datetime import UTC, datetime, timedelta
from typing import Annotated, Any

import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from passlib.context import CryptContext

from .db.models.user import User as UserService
from .db.models.role import Role as RoleService
from .schemas.token import TokenData
from .schemas.user import User

from app.core.settings import settings


SECRET_KEY = settings.JWT_SECRET_KEY
ALGORITHM = settings.JWT_ALG

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="api/token",
    scopes={
        "me": "Read information about the current user.",
        "create": "Create items",
        "read": "Read items",
        "update": "Update items",
        "delete": "Delete items",
    }
)

pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")



async def authenticate_user(username: str, password: str) -> dict[str, Any] | None:
    user = await UserService.all().filter(**{"username": username})
    if not user:
        return {}
    user_returned = user[0]
    role = await RoleService.all().filter(**{"id": user_returned.role_id})

    if user_returned is not None and not verify_password(password, user_returned.password):
        return {}
    return user_returned, role[0]


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)]) -> dict[str, Any] | None:
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub", None)
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(username=username, scopes=token_scopes)
    except InvalidTokenError as err:
        raise credentials_exception from err
    user = await UserService.all().filter(**{"username": token_data.username})
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user[0]


async def get_current_active_user(
    current_user: Annotated[User, Security(get_current_user, scopes=["me"])],
) -> User:
    return current_user