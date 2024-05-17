import json

from litestar import Response


class JSONResponse(Response):
    def __init__(self, status_code, content: dict):
        super().__init__(
            status_code=status_code,
            media_type="application/json",
            content=json.dumps(content),
        )


class EvidentlyServiceError(Exception):
    def to_response(self) -> Response:
        raise NotImplementedError


class EntityNotFound(EvidentlyServiceError):
    entity_name: str = ""

    def to_response(self) -> Response:
        return JSONResponse(
            status_code=404,
            content={"detail": f"{self.entity_name} not found"},
        )


class ProjectNotFound(EntityNotFound):
    entity_name = "Project"


class TeamNotFound(EntityNotFound):
    entity_name = "Team"


class UserNotFound(EntityNotFound):
    entity_name = "User"


class NotEnoughPermissions(EvidentlyServiceError):
    def to_response(self) -> Response:
        return JSONResponse(
            status_code=403,
            content={"detail": "Not enough permissions"},
        )


class NotAuthorized(EvidentlyServiceError):
    def to_response(self) -> Response:
        return JSONResponse(
            status_code=401,
            content={"detail": "Not authorized"},
        )
