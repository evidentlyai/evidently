from starlette.responses import JSONResponse
from starlette.responses import Response


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
