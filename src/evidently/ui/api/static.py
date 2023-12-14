import os
from typing import Callable

from fastapi import Depends
from fastapi import FastAPI
from fastapi import Request
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from evidently.ui.api.utils import event_logger


def add_static(app: FastAPI, ui_path: str):
    static_path = os.path.join(ui_path, "static")
    environment_path = os.environ.get("UI_ENVIRONMENT_PATH", static_path)
    app.mount("/static", StaticFiles(directory=static_path), name="static")
    app.mount("/env", StaticFiles(directory=environment_path), name="env")

    @app.get("/", include_in_schema=False)
    @app.get("/auth", include_in_schema=False)
    @app.get("/projects", include_in_schema=False)
    @app.get("/projects/{path:path}", include_in_schema=False)
    @app.get("/teams", include_in_schema=False)
    @app.get("/teams/{path:path}", include_in_schema=False)
    @app.get("/token", include_in_schema=False)
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
