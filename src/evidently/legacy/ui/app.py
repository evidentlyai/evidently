import os

import uvicorn

from evidently._pydantic_compat import SecretStr
from evidently.legacy.ui.components.base import AppBuilder
from evidently.legacy.ui.components.storage import LocalStorageComponent
from evidently.legacy.ui.config import AppConfig
from evidently.legacy.ui.config import load_config
from evidently.legacy.ui.config import settings
from evidently.legacy.ui.local_service import LocalConfig
from evidently.legacy.ui.security.token import TokenSecurityComponent
from evidently.legacy.ui.storage.common import EVIDENTLY_SECRET_ENV


def create_app(config: AppConfig):
    with config.context() as ctx:
        builder = AppBuilder(ctx)
        ctx.apply(builder)
        app = builder.build()
        ctx.finalize(app)
        return app


def run(config: AppConfig):
    app = create_app(config)
    uvicorn.run(app, host=config.service.host, port=config.service.port)


def get_config(
    host: str = "127.0.0.1",
    port: int = 8000,
    workspace: str = "workspace",
    secret: str = None,
    conf_path: str = None,
):
    settings.configure(settings_module=conf_path)
    config = load_config(LocalConfig, settings)
    config.service.host = host
    config.service.port = port
    if not isinstance(config.storage, LocalStorageComponent):
        raise ValueError("Storage component is not a LocalStorageComponent")
    config.storage.path = workspace

    secret = secret or os.environ.get(EVIDENTLY_SECRET_ENV)
    if secret is not None:
        config.security = TokenSecurityComponent(token=SecretStr(secret))

    return config


def run_local(
    host: str = "127.0.0.1",
    port: int = 8000,
    workspace: str = "workspace",
    secret: str = None,
    conf_path: str = None,
):
    config = get_config(host=host, port=port, workspace=workspace, secret=secret, conf_path=conf_path)
    run(config)


def litestar_app():
    config = get_config()
    return create_app(config)


def main():
    run_local()


if __name__ == "__main__":
    main()
