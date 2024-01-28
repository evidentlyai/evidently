from functools import partial
from typing import Callable

from fastapi import Depends
from iterative_telemetry import IterativeTelemetryLogger
from starlette.requests import Request

import evidently
from evidently.ui.api.security import is_authorized
from evidently.ui.config import Configuration
from evidently.ui.errors import NotEnoughPermissions


async def get_configuration(request: Request) -> Configuration:
    state = request.app.state
    if not hasattr(state, "config"):
        raise ValueError("Configuration isn't loaded")
    return state.config


_event_logger = None


def event_logger(
    config: Configuration = Depends(get_configuration),
):
    global _event_logger
    if _event_logger is None:
        _event_logger = IterativeTelemetryLogger(
            config.telemetry.tool_name,
            evidently.__version__,
            url=config.telemetry.url,
            token=config.telemetry.token,
            enabled=config.telemetry.enabled,
        )
    yield partial(_event_logger.send_event, config.telemetry.service_name)


async def authorized(is_authorized_: bool = Depends(is_authorized)):
    if not is_authorized_:
        raise NotEnoughPermissions()


def get_project_manager(
    request: Request,
    config: Configuration = Depends(get_configuration),
    log_event: Callable = Depends(event_logger),
):
    if not hasattr(request.app.state, "project_manager"):
        project_manager = config.storage.create_project_manager()
        if config.telemetry.enabled:
            print("Anonimous usage reporting is enabled")
        else:
            print("Anonimous usage reporting is disabled")
        log_event("startup")
        request.app.state.project_manager = project_manager
    try:
        yield request.app.state.project_manager
    finally:
        pass
