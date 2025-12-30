from typing import Annotated
from typing import Callable
from typing import List

from litestar import Router
from litestar import delete
from litestar import get
from litestar import post
from litestar import put
from litestar.params import Dependency

from evidently.sdk.artifacts import Artifact
from evidently.sdk.artifacts import ArtifactID
from evidently.sdk.artifacts import ArtifactVersion
from evidently.sdk.artifacts import ArtifactVersionID
from evidently.sdk.artifacts import VersionOrLatest
from evidently.ui.service.managers.artifacts import ArtifactManager
from evidently.ui.service.type_aliases import ProjectID
from evidently.ui.service.type_aliases import UserID


@get("")
async def list_artifacts(
    user_id: UserID,
    project_id: ProjectID,
    artifact_manager: Annotated[ArtifactManager, Dependency()],
) -> List[Artifact]:
    return await artifact_manager.list_artifacts(user_id, project_id)


@get("/{artifact_id:uuid}")
async def get_artifact(
    user_id: UserID,
    artifact_id: ArtifactID,
    artifact_manager: Annotated[ArtifactManager, Dependency()],
) -> Artifact:
    return await artifact_manager.get_artifact(user_id, artifact_id)


@get("/by-name/{name:str}")
async def get_artifact_by_name(
    user_id: UserID,
    project_id: ProjectID,
    name: str,
    artifact_manager: Annotated[ArtifactManager, Dependency()],
) -> Artifact:
    return await artifact_manager.get_artifact_by_name(user_id, project_id, name)


@post("")
async def add_artifact(
    user_id: UserID,
    project_id: ProjectID,
    data: Artifact,
    artifact_manager: Annotated[ArtifactManager, Dependency()],
) -> Artifact:
    return await artifact_manager.add_artifact(user_id, project_id, data)


@delete("/{artifact_id:uuid}")
async def delete_artifact(
    user_id: UserID,
    artifact_id: ArtifactID,
    artifact_manager: Annotated[ArtifactManager, Dependency()],
) -> None:
    await artifact_manager.delete_artifact(user_id, artifact_id)


@put("/{artifact_id:uuid}")
async def update_artifact(
    user_id: UserID,
    artifact_id: ArtifactID,
    data: Artifact,
    artifact_manager: Annotated[ArtifactManager, Dependency()],
) -> None:
    await artifact_manager.update_artifact(user_id, artifact_id, data)


@get("/{artifact_id:uuid}/versions")
async def list_artifact_versions(
    user_id: UserID,
    artifact_id: ArtifactID,
    artifact_manager: Annotated[ArtifactManager, Dependency()],
) -> List[ArtifactVersion]:
    return await artifact_manager.list_artifact_versions(user_id, artifact_id)


@get("/artifact-versions/{artifact_version_id:uuid}")
async def get_artifact_version(
    user_id: UserID,
    artifact_version_id: ArtifactVersionID,
    artifact_manager: Annotated[ArtifactManager, Dependency()],
) -> ArtifactVersion:
    return await artifact_manager.get_artifact_version(user_id, artifact_version_id)


@get("/{artifact_id:uuid}/versions/{version:str}")
async def get_artifact_version_by_version(
    user_id: UserID,
    artifact_id: ArtifactID,
    version: VersionOrLatest,
    artifact_manager: Annotated[ArtifactManager, Dependency()],
) -> ArtifactVersion:
    return await artifact_manager.get_artifact_version_by_version(user_id, artifact_id, version)


@post("/{artifact_id:uuid}/versions")
async def add_artifact_version(
    user_id: UserID,
    artifact_id: ArtifactID,
    data: ArtifactVersion,
    artifact_manager: Annotated[ArtifactManager, Dependency()],
) -> ArtifactVersion:
    return await artifact_manager.add_artifact_version(user_id, artifact_id, data)


@delete("/artifact-versions/{artifact_version_id:uuid}")
async def delete_artifact_version(
    user_id: UserID,
    artifact_version_id: ArtifactVersionID,
    artifact_manager: Annotated[ArtifactManager, Dependency()],
) -> None:
    await artifact_manager.delete_artifact_version(user_id, artifact_version_id)


def artifacts_router(guard: Callable) -> Router:
    return Router(
        path="/artifacts",
        route_handlers=[
            # read
            Router(
                "",
                route_handlers=[
                    list_artifacts,
                    get_artifact,
                    get_artifact_by_name,
                    list_artifact_versions,
                    get_artifact_version,
                    get_artifact_version_by_version,
                ],
            ),
            # write
            Router(
                "",
                route_handlers=[
                    add_artifact,
                    update_artifact,
                    delete_artifact,
                    add_artifact_version,
                    delete_artifact_version,
                ],
                guards=[guard],
            ),
        ],
    )
