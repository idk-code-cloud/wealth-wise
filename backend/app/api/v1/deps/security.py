from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer
from app.db.session import get_db
from app.utils.security import verify_token
from app.services.users import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/token")


async def get_current_user(
    token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_db)
):
    decoded_data = verify_token(token)
    if not decoded_data:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = await UserService(session).get_by_username(decoded_data["sub"])
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user
