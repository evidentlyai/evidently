import os
import pathlib
from typing import Callable

from litestar import Litestar
from litestar import Request
from litestar import Response
from litestar import Router

from evidently.ui.api.projects import project_api
from evidently.ui.api.service import service_api
from evidently.ui.components.base import AppBuilder
from evidently.ui.components.base import ComponentContext
from evidently.ui.components.base import ServiceComponent
from evidently.ui.components.security import NoSecurityConfig
from evidently.ui.components.security import SecurityComponent
from evidently.ui.components.storage import LocalStorageComponent
from evidently.ui.components.storage import StorageComponent
from evidently.ui.components.telemetry import TelemetryComponent
from evidently.ui.config import Config
from evidently.ui.errors import EvidentlyServiceError


def api_router(guard: Callable):
    return Router(path="/api", route_handlers=[project_api(guard), service_api()])


def unicorn_exception_handler(_: Request, exc: EvidentlyServiceError) -> Response:
    return exc.to_response()


class LocalServiceComponent(ServiceComponent):
    def apply(self, ctx: ComponentContext, builder: AppBuilder):
        super().apply(ctx, builder)
        builder.route_handlers.append(api_router(ctx.get_component(SecurityComponent).get_auth_guard()))
        builder.exception_handlers[EvidentlyServiceError] = unicorn_exception_handler
        builder.kwargs["debug"] = True

    def finalize(self, ctx: ComponentContext, app: Litestar):
        ui_path = os.path.join(pathlib.Path(__file__).parent.resolve(), "ui")
        from evidently.ui.api.static import add_static

        add_static(app, ui_path)


class LocalConfig(Config):
    security: SecurityComponent = NoSecurityConfig()
    service: ServiceComponent = LocalServiceComponent()
    storage: StorageComponent = LocalStorageComponent()
    telemetry: TelemetryComponent = TelemetryComponent()
