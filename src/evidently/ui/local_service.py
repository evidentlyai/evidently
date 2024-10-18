import logging
import time
from typing import Dict

from litestar import Request
from litestar import Response
from litestar.di import Provide
from litestar.logging import LoggingConfig

from evidently.ui.api.projects import create_projects_api
from evidently.ui.api.projects import projects_api_dependencies
from evidently.ui.api.service import service_api
from evidently.ui.api.static import assets_router
from evidently.ui.components.base import AppBuilder
from evidently.ui.components.base import ComponentContext
from evidently.ui.components.base import ServiceComponent
from evidently.ui.components.security import NoSecurityComponent
from evidently.ui.components.security import SecurityComponent
from evidently.ui.components.storage import LocalStorageComponent
from evidently.ui.components.storage import StorageComponent
from evidently.ui.components.telemetry import TelemetryComponent
from evidently.ui.config import AppConfig
from evidently.ui.config import ConfigContext
from evidently.ui.errors import EvidentlyServiceError


def evidently_service_exception_handler(_: Request, exc: EvidentlyServiceError) -> Response:
    return exc.to_response()


class LocalServiceComponent(ServiceComponent):
    debug: bool = False

    def get_api_route_handlers(self, ctx: ComponentContext):
        guard = ctx.get_component(SecurityComponent).get_auth_guard()
        return [create_projects_api(guard), service_api()]

    def get_dependencies(self, ctx: ComponentContext) -> Dict[str, Provide]:
        deps = super().get_dependencies(ctx)
        deps.update(projects_api_dependencies)
        return deps

    def get_route_handlers(self, ctx: ComponentContext):
        return [assets_router()]

    def apply(self, ctx: ComponentContext, builder: AppBuilder):
        super().apply(ctx, builder)
        assert isinstance(ctx, ConfigContext)
        builder.exception_handlers[EvidentlyServiceError] = evidently_service_exception_handler
        builder.kwargs["debug"] = self.debug
        if self.debug:
            log_config = create_logging()
            builder.kwargs["logging_config"] = LoggingConfig(**log_config)


def create_logging() -> dict:
    logging.Formatter.converter = time.gmtime
    return {
        "version": 1,
        "log_exceptions": "always",
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": "logging.Formatter",
                "format": "%(asctime)s %(levelname)-8s %(name)-15s %(message)s",
                "datefmt": "%Y-%m-%dT%H:%M:%SZ",
            },
            "access": {
                "()": "logging.Formatter",
                "format": "%(asctime)s %(levelname)-8s %(name)-15s %(message)s",
                "datefmt": "%Y-%m-%dT%H:%M:%SZ",
            },
            "standard": {
                "()": "logging.Formatter",
                "format": "%(asctime)s %(levelname)-8s %(name)-15s %(message)s",
                "datefmt": "%Y-%m-%dT%H:%M:%SZ",
            },
        },
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
            "access": {
                "formatter": "access",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "litestar": {"handlers": ["default"]},
            "uvicorn": {"handlers": ["default"], "level": "INFO", "propagate": False},
            "uvicorn.error": {"level": "INFO"},
            "uvicorn.access": {"handlers": ["access"], "level": "INFO", "propagate": False},
        },
    }


class LocalConfig(AppConfig):
    security: SecurityComponent = NoSecurityComponent()
    service: ServiceComponent = LocalServiceComponent()
    storage: StorageComponent = LocalStorageComponent()
    telemetry: TelemetryComponent = TelemetryComponent()
