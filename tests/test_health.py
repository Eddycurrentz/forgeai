from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient

from forgeai_api.api.health import overall_status


def test_overall_status_ok() -> None:
    assert overall_status(postgres=True, redis=True) == "ok"


def test_overall_status_degraded() -> None:
    assert overall_status(postgres=True, redis=False) == "degraded"


@pytest.mark.asyncio
async def test_health_ok_when_dependencies_respond(client: AsyncClient) -> None:
    with (
        patch("forgeai_api.api.health.ping_database", new_callable=AsyncMock, return_value=True),
        patch("forgeai_api.api.health.ping_redis", new_callable=AsyncMock, return_value=True),
    ):
        response = await client.get("/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["postgres"] is True
    assert payload["redis"] is True
    assert payload["service"] == "forgeai"
    assert "version" in payload


@pytest.mark.asyncio
async def test_health_degraded_when_postgres_unavailable(client: AsyncClient) -> None:
    with (
        patch(
            "forgeai_api.api.health.ping_database",
            new_callable=AsyncMock,
            side_effect=ConnectionError("db down"),
        ),
        patch("forgeai_api.api.health.ping_redis", new_callable=AsyncMock, return_value=True),
    ):
        response = await client.get("/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "degraded"
    assert payload["postgres"] is False
    assert payload["redis"] is True
