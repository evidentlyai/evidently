import os

import uvicorn

from evidently._pydantic_compat import SecretStr
from evidently.ui.components.base import AppBuilder
from evidently.ui.config import Config
from evidently.ui.config import load_config
from evidently.ui.config import settings
from evidently.ui.local_service import LocalConfig
from evidently.ui.security.token import TokenSecurityComponent
from evidently.ui.storage.common import EVIDENTLY_SECRET_ENV


def create_app(config: Config):
    with config.context() as ctx:
        builder = AppBuilder(ctx)
        ctx.apply(builder)
        app = builder.build()
        ctx.finalize(app)
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
    return_litestar_app: bool = False,
):
    settings.configure(settings_module=conf_path)
    config = load_config(LocalConfig, settings)
    config.service.host = host
    config.service.port = port
    config.storage.path = workspace

    secret = secret or os.environ.get(EVIDENTLY_SECRET_ENV)
    if secret is not None:
        config.security = TokenSecurityComponent(token=SecretStr(secret))

    if return_litestar_app:
        return create_app(config)

    run(config)


def litestar_app():
    return run_local(return_litestar_app=True)


def main():
    run_local()


if __name__ == "__main__":
    main()
