import os
import pathlib

from litestar import Litestar
from litestar import Request
from litestar import Response

from evidently.ui.api.projects import project_api
from evidently.ui.api.service import service_api
from evidently.ui.components.base import AppBuilder
from evidently.ui.components.base import ComponentContext
from evidently.ui.components.base import ServiceComponent
from evidently.ui.components.security import NoSecurityComponent
from evidently.ui.components.security import SecurityComponent
from evidently.ui.components.storage import LocalStorageComponent
from evidently.ui.components.storage import StorageComponent
from evidently.ui.components.telemetry import TelemetryComponent
from evidently.ui.config import Config
from evidently.ui.errors import EvidentlyServiceError


def evidently_service_exception_handler(_: Request, exc: EvidentlyServiceError) -> Response:
    return exc.to_response()


class LocalServiceComponent(ServiceComponent):
    def get_api_route_handelers(self, ctx: ComponentContext):
        guard = ctx.get_component(SecurityComponent).get_auth_guard()
        return [project_api(guard), service_api()]

    def apply(self, ctx: ComponentContext, builder: AppBuilder):
        super().apply(ctx, builder)
        builder.exception_handlers[EvidentlyServiceError] = evidently_service_exception_handler
        builder.kwargs["debug"] = True

    def finalize(self, ctx: ComponentContext, app: Litestar):
        ui_path = os.path.join(pathlib.Path(__file__).parent.resolve(), "ui")
        from evidently.ui.api.static import add_static

        add_static(app, ui_path)


class LocalConfig(Config):
    security: SecurityComponent = NoSecurityComponent()
    service: ServiceComponent = LocalServiceComponent()
    storage: StorageComponent = LocalStorageComponent()
    telemetry: TelemetryComponent = TelemetryComponent()
