from fastapi import Request

from forgeai_api.core.config import Settings
from forgeai_api.core.state import AppState


def get_request_settings(request: Request) -> Settings:
    settings = request.app.state.settings
    if not isinstance(settings, Settings):
        raise RuntimeError("application settings are not initialized")
    return settings


def get_request_runtime(request: Request) -> AppState:
    runtime = request.app.state.runtime
    if not isinstance(runtime, AppState):
        raise RuntimeError("application runtime is not initialized")
    return runtime
