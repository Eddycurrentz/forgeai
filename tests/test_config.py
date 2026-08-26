from forgeai_api.core.config import Settings


def test_settings_read_explicit_values() -> None:
    settings = Settings(
        app_env="test",
        api_port=8001,
        database_url="postgresql+asyncpg://forgeai:forgeai@db:5432/forgeai",
        redis_url="redis://cache:6379/1",
    )

    assert settings.app_env == "test"
    assert settings.api_port == 8001
    assert settings.async_database_url().startswith("postgresql+asyncpg://")
    assert settings.redis_url_str().startswith("redis://")
