class EvidentlyServiceError(Exception):
    pass


class EntityNotFound(EvidentlyServiceError):
    entity_name: str = ""


class ProjectNotFound(EntityNotFound):
    entity_name = "Project"


class TeamNotFound(EntityNotFound):
    entity_name = "Team"


class UserNotFound(EntityNotFound):
    entity_name = "User"


class NotEnoughPermissions(EvidentlyServiceError):
    pass


class NotAuthorized(EvidentlyServiceError):
    pass
