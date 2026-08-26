from fastapi import APIRouter, Request
from pydantic import BaseModel, Field

from forgeai_api import __version__
from forgeai_api.api.deps import get_request_runtime, get_request_settings
from forgeai_api.core.db import ping_database
from forgeai_api.core.redis import ping_redis

router = APIRouter()


class HealthResponse(BaseModel):
    status: str
    service: str
    environment: str
    postgres: bool
    redis: bool
    version: str = Field(description="API package version")


def overall_status(*, postgres: bool, redis: bool) -> str:
    return "ok" if postgres and redis else "degraded"


@router.get("/health", response_model=HealthResponse)
async def health(request: Request) -> HealthResponse:
    settings = get_request_settings(request)
    state = get_request_runtime(request)

    postgres_ok = False
    redis_ok = False
    try:
        postgres_ok = await ping_database(state.engine)
    except Exception:
        postgres_ok = False
    try:
        redis_ok = await ping_redis(state.redis)
    except Exception:
        redis_ok = False

    return HealthResponse(
        status=overall_status(postgres=postgres_ok, redis=redis_ok),
        service=settings.app_name,
        environment=settings.app_env,
        postgres=postgres_ok,
        redis=redis_ok,
        version=__version__,
    )
