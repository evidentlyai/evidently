from abc import ABC
from abc import abstractmethod
from typing import List
from typing import Optional

from evidently.legacy.ui.managers.base import BaseDependant
from evidently.sdk.artifacts import Artifact
from evidently.sdk.artifacts import ArtifactID
from evidently.sdk.artifacts import ArtifactVersion
from evidently.sdk.artifacts import ArtifactVersionID
from evidently.sdk.artifacts import VersionOrLatest
from evidently.ui.service.type_aliases import ProjectID


class ArtifactStorage(BaseDependant, ABC):
    @abstractmethod
    async def list_artifacts(self, project_id: ProjectID) -> List[Artifact]:
        raise NotImplementedError

    @abstractmethod
    async def get_artifact(self, artifact_id: ArtifactID) -> Optional[Artifact]:
        raise NotImplementedError

    @abstractmethod
    async def get_artifact_by_name(self, project_id: ProjectID, name: str) -> Optional[Artifact]:
        raise NotImplementedError

    @abstractmethod
    async def add_artifact(self, project_id: ProjectID, artifact: Artifact) -> Artifact:
        raise NotImplementedError

    @abstractmethod
    async def delete_artifact(self, artifact_id: ArtifactID) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_artifact(self, artifact_id: ArtifactID, artifact: Artifact) -> None:
        raise NotImplementedError

    @abstractmethod
    async def list_artifact_versions(self, artifact_id: ArtifactID) -> List[ArtifactVersion]:
        raise NotImplementedError

    @abstractmethod
    async def get_artifact_version(self, artifact_version_id: ArtifactVersionID) -> Optional[ArtifactVersion]:
        raise NotImplementedError

    @abstractmethod
    async def get_artifact_version_by_version(
        self, artifact_id: ArtifactID, version: VersionOrLatest
    ) -> Optional[ArtifactVersion]:
        raise NotImplementedError

    @abstractmethod
    async def add_artifact_version(self, artifact_id: ArtifactID, artifact_version: ArtifactVersion) -> ArtifactVersion:
        raise NotImplementedError

    @abstractmethod
    async def delete_artifact_version(self, artifact_version_id: ArtifactVersionID) -> None:
        raise NotImplementedError
