from typing import Annotated
from typing import Callable
from typing import List

from litestar import Router
from litestar import delete
from litestar import get
from litestar import post
from litestar import put
from litestar.params import Dependency

from evidently.llm.prompts.content import ArtifactPromptContent
from evidently.llm.prompts.content import PromptContent
from evidently.sdk.artifacts import Artifact
from evidently.sdk.artifacts import ArtifactMetadata
from evidently.sdk.artifacts import ArtifactVersion
from evidently.sdk.artifacts import ArtifactVersionMetadata
from evidently.sdk.prompts import Prompt
from evidently.sdk.prompts import PromptID
from evidently.sdk.prompts import PromptMetadata
from evidently.sdk.prompts import PromptVersion
from evidently.sdk.prompts import PromptVersionID
from evidently.sdk.prompts import PromptVersionMetadata
from evidently.sdk.prompts import VersionOrLatest
from evidently.ui.service.managers.artifacts import ArtifactManager
from evidently.ui.service.type_aliases import ProjectID
from evidently.ui.service.type_aliases import UserID


def _artifact_to_prompt(artifact: Artifact) -> Prompt:
    """Convert artifact to prompt."""
    return Prompt(
        id=artifact.id,
        project_id=artifact.project_id,
        name=artifact.name,
        metadata=PromptMetadata(
            created_at=artifact.metadata.created_at,
            updated_at=artifact.metadata.updated_at,
            author=artifact.metadata.author,
        ),
    )


def _artifact_version_to_prompt_version(artifact_version: ArtifactVersion) -> PromptVersion:
    """Convert artifact version to prompt version."""
    # Extract PromptContent from ArtifactPromptContent
    content = artifact_version.content
    if isinstance(content, ArtifactPromptContent):
        prompt_content = content.get_value()
    else:
        # Try to parse as PromptContent
        prompt_content = PromptContent.parse(content.data)

    return PromptVersion(
        id=artifact_version.id,
        prompt_id=artifact_version.artifact_id,
        version=artifact_version.version,
        content=prompt_content,
        metadata=PromptVersionMetadata(
            created_at=artifact_version.metadata.created_at,
            updated_at=artifact_version.metadata.updated_at,
            author=artifact_version.metadata.author,
        ),
    )


def _prompt_to_artifact(prompt: Prompt) -> Artifact:
    """Convert prompt to artifact."""
    return Artifact(
        id=prompt.id,
        project_id=prompt.project_id,
        name=prompt.name,
        metadata=ArtifactMetadata(
            created_at=prompt.metadata.created_at,
            updated_at=prompt.metadata.updated_at,
            author=prompt.metadata.author,
        ),
    )


def _prompt_version_to_artifact_version(prompt_version: PromptVersion) -> ArtifactVersion:
    """Convert prompt version to artifact version."""
    # Wrap PromptContent in ArtifactPromptContent
    # The content should already be parsed as PromptContent by PromptVersion.__init__,
    # but we handle the case where it might not be for safety
    content = prompt_version.content
    if not isinstance(content, PromptContent):
        content = PromptContent.parse(content)
    artifact_content = ArtifactPromptContent.from_value(content)

    return ArtifactVersion(
        id=prompt_version.id,
        artifact_id=prompt_version.prompt_id,
        version=prompt_version.version,
        content=artifact_content,
        metadata=ArtifactVersionMetadata(
            created_at=prompt_version.metadata.created_at,
            updated_at=prompt_version.metadata.updated_at,
            author=prompt_version.metadata.author,
        ),
    )


@get("")
async def list_prompts(
    user_id: UserID,
    project_id: ProjectID,
    artifact_manager: Annotated[ArtifactManager, Dependency()],
) -> List[Prompt]:
    artifacts = await artifact_manager.list_artifacts(user_id, project_id)
    return [_artifact_to_prompt(a) for a in artifacts]


@get("/{prompt_id:uuid}")
async def get_prompt(
    user_id: UserID,
    prompt_id: PromptID,
    artifact_manager: Annotated[ArtifactManager, Dependency()],
) -> Prompt:
    artifact = await artifact_manager.get_artifact(user_id, prompt_id)
    return _artifact_to_prompt(artifact)


@get("/by-name/{name:str}")
async def get_prompt_by_name(
    user_id: UserID,
    project_id: ProjectID,
    name: str,
    artifact_manager: Annotated[ArtifactManager, Dependency()],
) -> Prompt:
    artifact = await artifact_manager.get_artifact_by_name(user_id, project_id, name)
    return _artifact_to_prompt(artifact)


@post("")
async def add_prompt(
    user_id: UserID,
    project_id: ProjectID,
    data: Prompt,
    artifact_manager: Annotated[ArtifactManager, Dependency()],
) -> Prompt:
    artifact = _prompt_to_artifact(data)
    added_artifact = await artifact_manager.add_artifact(user_id, project_id, artifact)
    return _artifact_to_prompt(added_artifact)


@delete("/{prompt_id:uuid}")
async def delete_prompt(
    user_id: UserID,
    prompt_id: PromptID,
    artifact_manager: Annotated[ArtifactManager, Dependency()],
) -> None:
    await artifact_manager.delete_artifact(user_id, prompt_id)


@put("/{prompt_id:uuid}")
async def update_prompt(
    user_id: UserID,
    prompt_id: PromptID,
    data: Prompt,
    artifact_manager: Annotated[ArtifactManager, Dependency()],
) -> None:
    artifact = _prompt_to_artifact(data)
    await artifact_manager.update_artifact(user_id, prompt_id, artifact)


@get("/{prompt_id:uuid}/versions")
async def list_prompt_versions(
    user_id: UserID,
    prompt_id: PromptID,
    artifact_manager: Annotated[ArtifactManager, Dependency()],
) -> List[PromptVersion]:
    artifact_versions = await artifact_manager.list_artifact_versions(user_id, prompt_id)
    return [_artifact_version_to_prompt_version(av) for av in artifact_versions]


@get("/prompt-versions/{prompt_version_id:uuid}")
async def get_prompt_version(
    user_id: UserID,
    prompt_version_id: PromptVersionID,
    artifact_manager: Annotated[ArtifactManager, Dependency()],
) -> PromptVersion:
    artifact_version = await artifact_manager.get_artifact_version(user_id, prompt_version_id)
    return _artifact_version_to_prompt_version(artifact_version)


@get("/{prompt_id:uuid}/versions/{version:str}")
async def get_prompt_version_by_version(
    user_id: UserID,
    prompt_id: PromptID,
    version: VersionOrLatest,
    artifact_manager: Annotated[ArtifactManager, Dependency()],
) -> PromptVersion:
    artifact_version = await artifact_manager.get_artifact_version_by_version(user_id, prompt_id, version)
    return _artifact_version_to_prompt_version(artifact_version)


@post("/{prompt_id:uuid}/versions")
async def add_prompt_version(
    user_id: UserID,
    prompt_id: PromptID,
    data: PromptVersion,
    artifact_manager: Annotated[ArtifactManager, Dependency()],
) -> PromptVersion:
    artifact_version = _prompt_version_to_artifact_version(data)
    added_version = await artifact_manager.add_artifact_version(user_id, prompt_id, artifact_version)
    return _artifact_version_to_prompt_version(added_version)


@delete("/prompt-versions/{prompt_version_id:uuid}")
async def delete_prompt_version(
    user_id: UserID,
    prompt_version_id: PromptVersionID,
    artifact_manager: Annotated[ArtifactManager, Dependency()],
) -> None:
    await artifact_manager.delete_artifact_version(user_id, prompt_version_id)


def prompts_router(guard: Callable) -> Router:
    return Router(
        path="/prompts",
        route_handlers=[
            # read
            Router(
                "",
                route_handlers=[
                    list_prompts,
                    get_prompt,
                    get_prompt_by_name,
                    list_prompt_versions,
                    get_prompt_version,
                    get_prompt_version_by_version,
                ],
            ),
            # write
            Router(
                "",
                route_handlers=[
                    add_prompt,
                    update_prompt,
                    delete_prompt,
                    add_prompt_version,
                    delete_prompt_version,
                ],
                guards=[guard],
            ),
        ],
    )
