from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.repo.base import BaseRepository
from app.models import users as models


class UserRepository(BaseRepository[models.User]):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, id: int) -> Optional[models.User]:
        stmt = select(models.User).where(models.User.id == id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, username: str, hashed_password: str) -> models.User:
        user = models.User(username=username, hashed_password=hashed_password)
        user_info = models.UserInfo(user_id=user.id)

        user.info = user_info

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user

    async def get_all(self) -> Optional[List[models.User]]:
        stmt = select(models.User)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def delete_by_id(self, user_id: int) -> None:
        user = await self.get_by_id(user_id)
        if user:
            self.session.delete(user)
            await self.session.commit()

    async def count(self) -> int:
        stmt = select(models.User).count()
        return await self.session.execute(stmt)

    async def exists_by_id(self, user_id: int) -> bool:
        stmt = select(models.User).where(models.User.id == user_id)
        return await self.session.execute(stmt).scalar_one_or_none() is not None

    async def exists_by_username(self, username: str) -> bool:
        stmt = select(models.User).where(models.User.username == username)
        return (await self.session.execute(stmt)).scalar_one_or_none() is not None

    async def get_by_username(self, username: str) -> Optional[models.User]:
        stmt = select(models.User).where(models.User.username == username)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()