from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: PostgresDsn
    access_token_expire_minutes: int = 30
    algorithm: str = "HS256"
    secret_key: str

    model_config = SettingsConfigDict(env_file=".env")
