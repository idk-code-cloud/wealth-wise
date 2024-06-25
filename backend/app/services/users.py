from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.repo.users import UserRepository
from app.schemas import users as schemas
from app.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
)


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = UserRepository(session)

    async def create(self, user: schemas.UserCreate) -> schemas.User:
        """
        Create a new user in the database.

        Parameters:
        user (schemas.UserCreate): The user data to be created. It should include username and password.

        Returns:
        schemas.User: The newly created user with its ID.

        Raises:
        HTTPException: If the username already exists in the database, a 409 Conflict status code is raised.

        """
        if await self.repo.exists_by_username(user.username):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Username already exists"
            )
        hashed_password = hash_password(user.password)
        new_user = await self.repo.create(user.username, hashed_password)
        return schemas.User.model_validate(new_user)

    async def authenticate(self, username: str, password: str) -> schemas.Token:
        if (user := await self.repo.get_by_username(username)) is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
            )

        if not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
            )

        access_token = create_access_token({"sub": user.username})
        return schemas.Token(access_token=access_token, token_type="bearer")

    async def get_by_id(self, user_id: int) -> Optional[schemas.User]:
        if (user := await self.repo.get_by_id(user_id)) is None:
            return None
        return schemas.User.model_validate(user)

    async def get_by_username(self, username: str) -> Optional[schemas.User]:
        if (user := await self.repo.get_by_username(username)) is None:
            return None
        return schemas.User.model_validate(user)
