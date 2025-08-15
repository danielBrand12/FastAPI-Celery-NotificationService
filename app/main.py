# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from tortoise import Tortoise
from typing import Annotated
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from starlette.middleware.cors import CORSMiddleware

from app.api.api import api_router

from app.db.register import register_orm

from app.security import authenticate_user, create_access_token
from app.schemas.token import Token

from app.debug import initialize_fastapi_server_debugger_if_needed


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:

    # app startup
    initialize_fastapi_server_debugger_if_needed()

    # Create a new client and connect to the server
    await register_orm(app)

    yield
    # app shutdown
    await Tortoise.close_connections()



app = FastAPI(
    title="Sales app",
    lifespan=lifespan,
    
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")


@app.get("/")
async def get():
    return RedirectResponse(url="/docs")

@app.post("/api/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user, role = await authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=1440)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": role.scopes}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer", user_id=user.id, name=user.name,)


