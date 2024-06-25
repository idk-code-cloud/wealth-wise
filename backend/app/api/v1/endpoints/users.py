from typing import Annotated
from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.deps.security import get_current_user
from app.schemas import users as schemas
from app.schemas.errors import HTTPError
from app.services.users import UserService
from app.db.session import get_db

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/",
    response_model=schemas.User,
    responses={
        status.HTTP_409_CONFLICT: {
            "description": "Username already exists",
            "model": HTTPError,
        },
    },
)
async def create_user(
    user: schemas.UserCreate, session: AsyncSession = Depends(get_db)
) -> schemas.User:
    return await UserService(session).create(user)


@router.post(
    "/token",
    response_model=schemas.Token,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Invalid username or password",
            "model": HTTPError,
        }
    },
)
async def token(
    data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(get_db),
) -> schemas.Token:
    return await UserService(session).authenticate(data.username, data.password)


@router.get(
    "/",
    response_model=schemas.User,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "User not found",
            "model": HTTPError,
        }
    },
)
async def get_me(user: schemas.User = Depends(get_current_user)) -> schemas.User:
    return user
