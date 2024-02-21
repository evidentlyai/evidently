import os
import pathlib
from typing import Optional

import litestar
from litestar import Litestar
from litestar import MediaType
from litestar import Request
from litestar import Response
from litestar.static_files import StaticFilesConfig


def add_static(app: Litestar, ui_path: str):
    @litestar.get(
        [
            "/",
            "/projects",
            "/signup",
            "/auth",
            "/teams",
            "/token",
            "/projects/{path:path}",
            "/teams/{path:path}",
        ],
        include_in_schema=False,
    )
    async def index(path: Optional[str]) -> Response:
        data = open(pathlib.Path(ui_path) / "index.html").read()
        return Response(content=data, media_type=MediaType.HTML)

    @litestar.get(
        [
            "/manifest.json",
            "/favicon.ico",
            "/favicon-16x16.png",
            "/favicon-32x32.png",
        ],
        include_in_schema=False,
    )
    async def manifest(request: Request) -> Response:
        path = request.url.path[1:]
        if path in ("manifest.json", "favicon.ico", "favicon-16x16.png", "favicon-32x32.png"):
            data = os.path.join(ui_path, path)
            with open(data, "rb") as f:
                return Response(content=f.read())
        return Response(content="not found", status_code=404)

    app.register(index)
    app.register(manifest)
    app.register(StaticFilesConfig("/static", directories=[pathlib.Path(ui_path) / "static"]).to_static_files_app())
