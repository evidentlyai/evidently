from typing import Callable

from fastapi import Depends
from starlette.requests import Request

from evidently.ui.config import Configuration
from evidently.ui.config import get_configuration
from evidently.ui.utils import event_logger


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
