from evidently.ui.components.base import AppBuilder
from evidently.ui.config import load_config
from evidently.ui.config import settings
from evidently.ui.local_service import LocalConfig


def create_app():
    config = load_config(LocalConfig, settings)

    with config.context() as ctx:
        builder = AppBuilder(ctx)
        ctx.apply(builder)
        app = builder.build()
        ctx.finalize(app)
        return app
