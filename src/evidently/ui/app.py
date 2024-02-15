import os
import pathlib
from functools import partial
from typing import Any

import uvicorn
from iterative_telemetry import IterativeTelemetryLogger
from litestar import Litestar
from litestar import Request
from litestar import Response
from litestar import Router
from litestar.di import Provide

import evidently
from evidently.ui.api.projects import project_api
from evidently.ui.api.security import get_org_id
from evidently.ui.api.security import get_user_id
from evidently.ui.api.service import service_api
from evidently.ui.api.static import add_static
from evidently.ui.base import AuthManager
from evidently.ui.base import BlobStorage
from evidently.ui.base import DataStorage
from evidently.ui.base import MetadataStorage
from evidently.ui.base import ProjectManager
from evidently.ui.config import Config
from evidently.ui.config import load_config
from evidently.ui.config import settings
from evidently.ui.errors import EvidentlyServiceError
from evidently.ui.storage.common import NoopAuthManager
from evidently.ui.storage.local import FSSpecBlobStorage
from evidently.ui.storage.local import InMemoryDataStorage
from evidently.ui.storage.local import JsonFileMetadataStorage


def api_router():
    return Router(path="/api", route_handlers=[project_api(), service_api()])


def unicorn_exception_handler(_: Request, exc: EvidentlyServiceError) -> Response:
    resp = exc.to_response()
    return Response(
        status_code=resp.status_code,
        content=resp.body,
        headers=resp.headers,
        media_type=resp.media_type,
    )


async def get_event_logger(telemetry_config: Any):
    _event_logger = IterativeTelemetryLogger(
        telemetry_config.tool_name,
        evidently.__version__,
        url=telemetry_config.url,
        token=telemetry_config.token,
        enabled=telemetry_config.enabled,
    )
    yield partial(_event_logger.send_event, telemetry_config.service_name)


async def create_project_manager(
    metadata_storage: MetadataStorage,
    data_storage: DataStorage,
    blob_storage: BlobStorage,
    auth_manager: AuthManager,
):
    return ProjectManager(
        metadata=metadata_storage,
        data=data_storage,
        blob=blob_storage,
        auth=auth_manager,
    )


def run(config: Config):
    ui_path = os.path.join(pathlib.Path(__file__).parent.resolve(), "ui")
    app = Litestar(
        route_handlers=[
            api_router(),
        ],
        exception_handlers={
            EvidentlyServiceError: unicorn_exception_handler,
        },
        dependencies={
            "telemetry_config": Provide(lambda: config.telemetry, sync_to_thread=True),
            "metadata_storage": Provide(
                lambda: JsonFileMetadataStorage(path=config.storage.metadata.path),
                sync_to_thread=True,
                use_cache=True,
            ),
            "data_storage": Provide(
                lambda: InMemoryDataStorage(path=config.storage.data.path),
                sync_to_thread=True,
                use_cache=True,
            ),
            "blob_storage": Provide(
                lambda: FSSpecBlobStorage(base_path=config.storage.blob.path),
                sync_to_thread=True,
                use_cache=True,
            ),
            "auth_manager": Provide(lambda: NoopAuthManager(), sync_to_thread=True, use_cache=True),
            "project_manager": Provide(create_project_manager, sync_to_thread=True, use_cache=True),
            "user_id": Provide(get_user_id),
            "org_id": Provide(get_org_id),
            "log_event": Provide(get_event_logger),
        },
        debug=True,
    )
    add_static(app, ui_path)
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
    config.storage.metadata.path = workspace
    config.storage.data.path = workspace
    config.storage.blob.path = workspace
    # secret = secret or os.environ.get(EVIDENTLY_SECRET_ENV)
    run(config)


def main():
    run_local()


if __name__ == "__main__":
    main()
