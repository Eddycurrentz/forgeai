from collections.abc import AsyncIterator

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from forgeai_api.core.config import Settings
from forgeai_api.main import create_app


@pytest.fixture
def settings() -> Settings:
    return Settings(
        app_name="forgeai",
        app_env="test",
        database_url="postgresql+asyncpg://forgeai:forgeai@localhost:5432/forgeai",
        database_url_sync="postgresql+psycopg://forgeai:forgeai@localhost:5432/forgeai",
        redis_url="redis://localhost:6379/0",
    )


@pytest.fixture
def app(settings: Settings) -> FastAPI:
    return create_app(settings)


@pytest.fixture
async def client(app: FastAPI) -> AsyncIterator[AsyncClient]:
    async with AsyncClient(
        transport=ASGITransport(app=app, lifespan="on"),
        base_url="http://test",
    ) as async_client:
        yield async_client
