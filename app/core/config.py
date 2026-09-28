from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    name: str = "FastAPI Backend"
    version: str = "0.1.0"
    debug: bool = False
    secret_key: str = "secretkey"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="APP_",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


PUBLIC_PATHS = frozenset(
    {
        "/docs",
        "/v1/health",
        "/v1/auth/signup",
        "/v1/auth/login",
        "/v1/auth/token",
    }
)
