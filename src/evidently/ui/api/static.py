import pathlib

import litestar
from litestar import MediaType
from litestar import Response
from litestar.response import File
from litestar.router import Router
from litestar.static_files import create_static_files_router

base_path = pathlib.Path(__file__).parent.parent.resolve() / "ui"


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
async def index() -> Response:
    return File(
        path=base_path.joinpath("index.html"),
        filename="index.html",
        media_type=MediaType.HTML,
        content_disposition_type="inline",
    )


assets_router = Router(
    path="",
    route_handlers=[
        index,
        create_static_files_router("/static", directories=[pathlib.Path(base_path) / "static"]),
        create_static_files_router("/", directories=[pathlib.Path(base_path) / "assets"]),
    ],
)
