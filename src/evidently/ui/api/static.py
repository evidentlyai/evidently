import os
import pathlib
from typing import Optional

import litestar
from litestar import MediaType
from litestar import Request
from litestar import Response
from litestar.response import File
from litestar.router import Router
from litestar.static_files import create_static_files_router


def create_static_routes(ui_path: str) -> Router:
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
        return File(path=pathlib.Path(ui_path).joinpath("index.html"), media_type=MediaType.HTML)

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
        return File(path=os.path.join(ui_path, path), content_disposition_type="inline")

    return Router(
        path="",
        route_handlers=[
            index,
            manifest,
            create_static_files_router("/static", directories=[pathlib.Path(ui_path) / "static"]),
        ],
    )
