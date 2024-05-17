import os
import pathlib
from functools import partial
from typing import Any
from typing import Callable
from typing import Optional

import uvicorn
from iterative_telemetry import IterativeTelemetryLogger
from litestar import Litestar
from litestar import Request
from litestar import Response
from litestar import Router
from litestar.connection import ASGIConnection
from litestar.di import Provide
from litestar.handlers import BaseRouteHandler
from litestar.types import ASGIApp
from litestar.types import Receive
from litestar.types import Scope
from litestar.types import Send

import evidently
from evidently.telemetry import DO_NOT_TRACK
from evidently.ui.api.projects import project_api
from evidently.ui.api.service import service_api
from evidently.ui.api.static import add_static
from evidently.ui.base import AuthManager
from evidently.ui.config import Config
from evidently.ui.config import load_config
from evidently.ui.config import settings
from evidently.ui.errors import EvidentlyServiceError
from evidently.ui.errors import NotEnoughPermissions
from evidently.ui.security.config import NoSecurityConfig
from evidently.ui.security.no_security import NoSecurityService
from evidently.ui.security.service import SecurityService
from evidently.ui.security.token import TokenSecurity
from evidently.ui.security.token import TokenSecurityConfig
from evidently.ui.storage.common import EVIDENTLY_SECRET_ENV
from evidently.ui.storage.common import NoopAuthManager
from evidently.ui.storage.local import create_local_project_manager
from evidently.ui.type_aliases import OrgID
from evidently.ui.type_aliases import UserID
from evidently.ui.utils import parse_json


def api_router(guard: Callable):
    return Router(path="/api", route_handlers=[project_api(guard), service_api()])


def unicorn_exception_handler(_: Request, exc: EvidentlyServiceError) -> Response:
    return exc.to_response()


async def get_user_id() -> UserID:
    return UserID("00000000-0000-0000-0000-000000000001")


async def get_org_id() -> Optional[OrgID]:
    return None


async def get_event_logger(telemetry_config: Any):
    _event_logger = IterativeTelemetryLogger(
        telemetry_config.tool_name,
        evidently.__version__,
        url=telemetry_config.url,
        token=telemetry_config.token,
        enabled=telemetry_config.enabled and DO_NOT_TRACK is None,
    )
    yield partial(_event_logger.send_event, telemetry_config.service_name)


def create_project_manager(
    path: str,
    auth_manager: AuthManager,
    autorefresh: bool,
):
    return create_local_project_manager(path, autorefresh, auth_manager)


def create_app(config: Config):
    config_security = config.security
    security: SecurityService
    if isinstance(config_security, NoSecurityConfig):
        security = NoSecurityService(config_security)
    elif isinstance(config_security, TokenSecurityConfig):
        security = TokenSecurity(config_security)

    def auth_middleware_factory(app: ASGIApp) -> ASGIApp:
        async def middleware(scope: Scope, receive: Receive, send: Send) -> None:
            request: Request = Request(scope)
            auth = security.authenticate(request)
            if auth is None:
                scope["auth"] = {
                    "authenticated": False,
                }
            else:
                scope["auth"] = {
                    "user_id": auth.id,
                    "org_id": auth.org_id,
                    "authenticated": True,
                }
            await app(scope, receive, send)

        return middleware

    def is_authenticated(connection: ASGIConnection, _: BaseRouteHandler) -> None:
        if not connection.scope["auth"]["authenticated"]:
            raise NotEnoughPermissions()

    ui_path = os.path.join(pathlib.Path(__file__).parent.resolve(), "ui")
    app = Litestar(
        route_handlers=[
            api_router(is_authenticated),
        ],
        exception_handlers={
            EvidentlyServiceError: unicorn_exception_handler,
        },
        dependencies={
            "telemetry_config": Provide(lambda: config.telemetry, sync_to_thread=True),
            "project_manager": Provide(
                lambda: create_project_manager(
                    config.storage.path, NoopAuthManager(), autorefresh=config.storage.autorefresh
                ),
                sync_to_thread=True,
                use_cache=True,
            ),
            "user_id": Provide(get_user_id),
            "org_id": Provide(get_org_id),
            "log_event": Provide(get_event_logger),
            "parsed_json": Provide(parse_json),
        },
        middleware=[auth_middleware_factory],
        debug=True,
    )
    add_static(app, ui_path)
    return app


def run(config: Config):
    app = create_app(config)
    uvicorn.run(app, host=config.service.host, port=config.service.port)


def run_local(
    host: str = "0.0.0.0",
    port: int = 8000,
    workspace: str = "workspace",
    secret: str = None,
    conf_path: str = None,
):
    settings.configure(settings_module=conf_path)
    config = load_config(Config)(settings)
    config.service.host = host
    config.service.port = port
    config.storage.path = workspace

    if secret or os.environ.get(EVIDENTLY_SECRET_ENV):
        config.security = TokenSecurityConfig(token=secret or os.environ.get(EVIDENTLY_SECRET_ENV))
    run(config)


def main():
    run_local()


if __name__ == "__main__":
    main()
