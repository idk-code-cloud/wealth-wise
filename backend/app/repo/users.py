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

    