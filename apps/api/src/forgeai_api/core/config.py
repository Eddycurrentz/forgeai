from functools import lru_cache

from pydantic import Field, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration loaded from environment variables and `.env`."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "forgeai"
    app_env: str = "development"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    log_level: str = "INFO"

    # SQLAlchemy URLs keep the driver suffix (`+asyncpg`, `+psycopg`), so these
    # are plain strings rather than PostgresDsn.
    database_url: str = Field(
        default="postgresql+asyncpg://forgeai:forgeai@localhost:5432/forgeai",
        min_length=1,
    )
    database_url_sync: str = Field(
        default="postgresql+psycopg://forgeai:forgeai@localhost:5432/forgeai",
        min_length=1,
    )
    redis_url: RedisDsn = Field(default=RedisDsn("redis://localhost:6379/0"))

    def async_database_url(self) -> str:
        return self.database_url

    def sync_database_url(self) -> str:
        return self.database_url_sync

    def redis_url_str(self) -> str:
        return str(self.redis_url)


@lru_cache
def get_settings() -> Settings:
    return Settings()
