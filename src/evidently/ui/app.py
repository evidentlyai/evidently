import os
import pathlib

import uvicorn
from fastapi import APIRouter
from fastapi import FastAPI
from fastapi import Request

from evidently.ui.api.projects import project_api
from evidently.ui.api.security import setup_security
from evidently.ui.api.service import service_api
from evidently.ui.api.static import add_static
from evidently.ui.config import Configuration
from evidently.ui.config import ServiceConfig
from evidently.ui.config import read_configuration
from evidently.ui.errors import EvidentlyServiceError
from evidently.ui.storage.common import EVIDENTLY_SECRET_ENV
from evidently.ui.storage.common import SecretHeaderSecurity
from evidently.ui.storage.local import LocalStorageConfig

app = FastAPI()

ui_path = os.path.join(pathlib.Path(__file__).parent.resolve(), "ui")
add_static(app, ui_path)

api_router = APIRouter(prefix="/api")

api_router.include_router(project_api)
api_router.include_router(service_api)
app.include_router(api_router)


@app.exception_handler(EvidentlyServiceError)
async def entity_not_found_exception_handler(request: Request, exc: EvidentlyServiceError):
    return exc.to_response()


def run(config: Configuration):
    app.state.config = config
    setup_security(app, config.security)
    uvicorn.run(app, host=config.service.host, port=config.service.port)


def run_local(
    host: str = "0.0.0.0", port: int = 8000, workspace: str = "workspace", secret: str = None, conf_path: str = None
):
    if conf_path is not None:
        config = read_configuration(conf_path)
        if config is None:
            raise ValueError(f"Config file not found at {conf_path}")
    else:
        config = Configuration(
            service=ServiceConfig(host=host, port=port), storage=LocalStorageConfig(path=workspace, autorefresh=True)
        )
        secret = secret or os.environ.get(EVIDENTLY_SECRET_ENV)
        if secret is not None:
            config.security = SecretHeaderSecurity(secret=secret)
    run(config)


def main():
    # conf_path = "service.yaml"
    run_local()


if __name__ == "__main__":
    main()
