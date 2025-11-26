from typing import Any
from typing import List
from typing import Optional

from evidently.sdk.artifacts import Artifact
from evidently.sdk.artifacts import ArtifactID
from evidently.sdk.artifacts import ArtifactVersion
from evidently.sdk.artifacts import ArtifactVersionID
from evidently.sdk.artifacts import ArtifactVersionMetadata
from evidently.sdk.artifacts import VersionOrLatest
from evidently.ui.service.base import EntityType
from evidently.ui.service.errors import ArtifactNotFound
from evidently.ui.service.errors import ArtifactVersionNotFound
from evidently.ui.service.errors import NotEnoughPermissions
from evidently.ui.service.managers.auth import AuthManager
from evidently.ui.service.managers.auth import Permission
from evidently.ui.service.managers.base import BaseManager
from evidently.ui.service.storage.artifacts import ArtifactStorage
from evidently.ui.service.type_aliases import ProjectID
from evidently.ui.service.type_aliases import UserID


class ArtifactManager(BaseManager):
    auth_manager: AuthManager
    artifact_storage: ArtifactStorage

    async def list_artifacts(self, user_id: UserID, project_id: ProjectID) -> List[Artifact]:
        if not await self.auth_manager.check_entity_permission(
            user_id, EntityType.Project, project_id, Permission.PROJECT_READ
        ):
            raise NotEnoughPermissions()
        return await self.artifact_storage.list_artifacts(project_id)

    async def get_artifact(self, user_id: UserID, artifact_id: ArtifactID) -> Artifact:
        # For now, we check project permission - in future might want artifact-specific permissions
        artifact = await self.artifact_storage.get_artifact(artifact_id)
        if artifact is None:
            raise ArtifactNotFound()
        if not await self.auth_manager.check_entity_permission(
            user_id, EntityType.Project, artifact.project_id, Permission.PROJECT_READ
        ):
            raise NotEnoughPermissions()
        return artifact

    async def get_artifact_by_name(self, user_id: UserID, project_id: ProjectID, name: str) -> Artifact:
        if not await self.auth_manager.check_entity_permission(
            user_id, EntityType.Project, project_id, Permission.PROJECT_READ
        ):
            raise NotEnoughPermissions()
        artifact = await self.artifact_storage.get_artifact_by_name(project_id, name)
        if artifact is None:
            raise ArtifactNotFound()
        return artifact

    async def add_artifact(self, user_id: UserID, project_id: ProjectID, artifact: Artifact) -> Artifact:
        if not await self.auth_manager.check_entity_permission(
            user_id, EntityType.Project, project_id, Permission.PROJECT_WRITE
        ):
            raise NotEnoughPermissions()
        artifact.project_id = project_id
        artifact.metadata.author = user_id
        return await self.artifact_storage.add_artifact(project_id, artifact)

    async def delete_artifact(self, user_id: UserID, artifact_id: ArtifactID) -> None:
        artifact = await self.artifact_storage.get_artifact(artifact_id)
        if artifact is None:
            raise ArtifactNotFound()
        if not await self.auth_manager.check_entity_permission(
            user_id, EntityType.Project, artifact.project_id, Permission.PROJECT_WRITE
        ):
            raise NotEnoughPermissions()
        return await self.artifact_storage.delete_artifact(artifact_id)

    async def update_artifact(self, user_id: UserID, artifact_id: ArtifactID, artifact: Artifact) -> None:
        existing = await self.artifact_storage.get_artifact(artifact_id)
        if existing is None:
            raise ArtifactNotFound()
        if not await self.auth_manager.check_entity_permission(
            user_id, EntityType.Project, existing.project_id, Permission.PROJECT_WRITE
        ):
            raise NotEnoughPermissions()
        return await self.artifact_storage.update_artifact(artifact_id, artifact)

    async def list_artifact_versions(self, user_id: UserID, artifact_id: ArtifactID) -> List[ArtifactVersion]:
        artifact = await self.artifact_storage.get_artifact(artifact_id)
        if artifact is None:
            raise ArtifactNotFound()
        if not await self.auth_manager.check_entity_permission(
            user_id, EntityType.Project, artifact.project_id, Permission.PROJECT_READ
        ):
            raise NotEnoughPermissions()
        return await self.artifact_storage.list_artifact_versions(artifact_id)

    async def get_artifact_version(self, user_id: UserID, artifact_version_id: ArtifactVersionID) -> ArtifactVersion:
        version = await self.artifact_storage.get_artifact_version(artifact_version_id)
        if version is None:
            raise ArtifactVersionNotFound()
        artifact = await self.artifact_storage.get_artifact(version.artifact_id)
        if artifact is None:
            raise ArtifactNotFound()
        if not await self.auth_manager.check_entity_permission(
            user_id, EntityType.Project, artifact.project_id, Permission.PROJECT_READ
        ):
            raise NotEnoughPermissions()
        return version

    async def get_artifact_version_by_version(
        self, user_id: UserID, artifact_id: ArtifactID, version: VersionOrLatest
    ) -> ArtifactVersion:
        artifact = await self.artifact_storage.get_artifact(artifact_id)
        if artifact is None:
            raise ArtifactNotFound()
        if not await self.auth_manager.check_entity_permission(
            user_id, EntityType.Project, artifact.project_id, Permission.PROJECT_READ
        ):
            raise NotEnoughPermissions()
        artifact_version = await self.artifact_storage.get_artifact_version_by_version(artifact_id, version)
        if artifact_version is None:
            raise ArtifactVersionNotFound()
        return artifact_version

    async def add_artifact_version(
        self, user_id: UserID, artifact_id: ArtifactID, artifact_version: ArtifactVersion
    ) -> ArtifactVersion:
        artifact = await self.artifact_storage.get_artifact(artifact_id)
        if artifact is None:
            raise ArtifactNotFound()
        if not await self.auth_manager.check_entity_permission(
            user_id, EntityType.Project, artifact.project_id, Permission.PROJECT_WRITE
        ):
            raise NotEnoughPermissions()
        artifact_version.artifact_id = artifact_id
        artifact_version.metadata.author = user_id
        return await self.artifact_storage.add_artifact_version(artifact_id, artifact_version)

    async def delete_artifact_version(self, user_id: UserID, artifact_version_id: ArtifactVersionID) -> None:
        version = await self.artifact_storage.get_artifact_version(artifact_version_id)
        if version is None:
            raise ArtifactVersionNotFound()
        artifact = await self.artifact_storage.get_artifact(version.artifact_id)
        if artifact is None:
            raise ArtifactNotFound()
        if not await self.auth_manager.check_entity_permission(
            user_id, EntityType.Project, artifact.project_id, Permission.PROJECT_WRITE
        ):
            raise NotEnoughPermissions()
        return await self.artifact_storage.delete_artifact_version(artifact_version_id)

    async def bump_artifact_version(
        self, user_id: UserID, artifact_id: ArtifactID, content: Any, metadata: Optional[ArtifactVersionMetadata] = None
    ) -> ArtifactVersion:
        try:
            v = await self.get_artifact_version_by_version(user_id, artifact_id, "latest")
            version = v.version + 1
        except ArtifactVersionNotFound:
            version = 1
        return await self.add_artifact_version(
            user_id,
            artifact_id,
            ArtifactVersion(
                content=content,
                version=version,
                artifact_id=artifact_id,
                metadata=metadata or ArtifactVersionMetadata(),
            ),
        )
