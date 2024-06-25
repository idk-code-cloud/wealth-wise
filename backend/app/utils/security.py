from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.utils.deps import get_settings

settings = get_settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )
    return encoded_jwt


def verify_token(token: str):
    payload = jwt.decode(token, settings.secret_key, algorithms=settings.algorithm)
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=settings.algorithm)
        return payload
    except JWTError:
        return None
