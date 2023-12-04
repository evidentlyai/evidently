import os
import pathlib
import sys
from typing import Callable

import uvicorn
from fastapi import APIRouter
from fastapi import Depends
from fastapi import FastAPI
from fastapi import Request
from starlette.responses import FileResponse
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles

from evidently.ui.api.projects import project_api
from evidently.ui.api.service import service_api
from evidently.ui.config import init_configuration
from evidently.ui.errors import EntityNotFound
from evidently.ui.errors import NotEnoughPermissions
from evidently.ui.utils import event_logger
from evidently.ui.utils import set_secret

app = FastAPI()

ui_path = os.path.join(pathlib.Path(__file__).parent.resolve(), "ui")
static_path = os.path.join(ui_path, "static")
environment_path = os.environ.get("UI_ENVIRONMENT_PATH", static_path)
app.mount("/static", StaticFiles(directory=static_path), name="static")
app.mount("/env", StaticFiles(directory=environment_path), name="env")


@app.get("/", include_in_schema=False)
@app.get("/auth", include_in_schema=False)
@app.get("/projects", include_in_schema=False)
@app.get("/projects/{path:path}", include_in_schema=False)
async def index(
    path=None,
    log_event: Callable = Depends(event_logger),
):
    log_event("index")
    return FileResponse(os.path.join(ui_path, "index.html"))


@app.get("/manifest.json", include_in_schema=False)
@app.get("/favicon.ico", include_in_schema=False)
@app.get("/favicon-16x16.png", include_in_schema=False)
@app.get("/favicon-32x32.png", include_in_schema=False)
@app.get("/env/env.js", include_in_schema=False)
async def manifest(request: Request):
    path = request.url.path[1:]
    if path in ("manifest.json", "favicon.ico", "favicon-16x16.png", "favicon-32x32.png", "env/env.js"):
        return FileResponse(os.path.join(ui_path, path))


api_router = APIRouter(prefix="/api")

api_router.include_router(project_api)
api_router.include_router(service_api)
app.include_router(api_router)


@app.exception_handler(EntityNotFound)
async def entity_not_found_exception_handler(request: Request, exc: EntityNotFound):
    return JSONResponse(
        status_code=404,
        content={"detail": f"{exc.entity_name} not found"},
    )


@app.exception_handler(NotEnoughPermissions)
async def not_enough_permissions_exception_handler(request: Request, exc: NotEnoughPermissions):
    return JSONResponse(
        status_code=403,
        content={"detail": "Not enough permissions"},
    )


def run_local(host: str = "0.0.0.0", port: int = 8000, workspace: str = "workspace", secret: str = None):
    if secret is not None:
        set_secret(secret)
    # todo: config
    # app.state.workspace = prepare_workspace(workspace)
    uvicorn.run(app, host=host, port=port)


def main():
    conf_path = "service.yaml"
    # tmp
    if len(sys.argv) > 1:
        conf_path = sys.argv[1]
        print(f"Loading conf from {conf_path}")
    config = init_configuration(conf_path)

    from evidently.ui.api.security import setup_security

    setup_security(app, config.security)
    uvicorn.run(app, host=config.service.host, port=config.service.port)


if __name__ == "__main__":
    main()
