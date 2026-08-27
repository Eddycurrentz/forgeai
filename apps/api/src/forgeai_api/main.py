from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from forgeai_api.api.health import router as health_router
from forgeai_api.api.repositories import router as repositories_router
from forgeai_api.api.runs import router as runs_router
from forgeai_api.core.config import Settings, get_settings
from forgeai_api.core.db import create_engine, create_session_factory
from forgeai_api.core.redis import create_redis_client
from forgeai_api.core.state import AppState


def create_app(settings: Settings | None = None) -> FastAPI:
    resolved = settings or get_settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        engine = create_engine(resolved)
        session_factory = create_session_factory(engine)
        redis_client = create_redis_client(resolved)
        app.state.settings = resolved
        app.state.runtime = AppState(
            engine=engine,
            session_factory=session_factory,
            redis=redis_client,
        )
        yield
        await redis_client.aclose()
        await engine.dispose()

    application = FastAPI(
        title="ForgeAI API",
        version="0.1.0",
        lifespan=lifespan,
    )
    application.include_router(health_router)
    application.include_router(repositories_router)
    application.include_router(runs_router)
    return application


app = create_app()
