import os
import pathlib
from typing import Callable

import uvicorn
from litestar import Litestar
from litestar import Request
from litestar import Response
from litestar import Router

from evidently.ui.api.projects import project_api
from evidently.ui.api.service import service_api
from evidently.ui.api.static import add_static
from evidently.ui.config import Config
from evidently.ui.config import LocalConfig
from evidently.ui.config import load_config
from evidently.ui.config import settings
from evidently.ui.errors import EvidentlyServiceError
from evidently.ui.security.token import TokenSecurityConfig
from evidently.ui.storage.common import EVIDENTLY_SECRET_ENV


def api_router(guard: Callable):
    return Router(path="/api", route_handlers=[project_api(guard), service_api()])


def unicorn_exception_handler(_: Request, exc: EvidentlyServiceError) -> Response:
    return exc.to_response()


def create_app(config: Config):
    with config.context():
        ui_path = os.path.join(pathlib.Path(__file__).parent.resolve(), "ui")
        app = Litestar(
            route_handlers=[
                api_router(config.security.get_auth_guard()),
            ],
            exception_handlers={
                EvidentlyServiceError: unicorn_exception_handler,
            },
            dependencies=config.get_dependencies(),
            middleware=config.get_middlewares(),
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
    config = load_config(LocalConfig, settings)
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
