import json
import posixpath
from typing import Dict
from typing import List
from typing import Optional

from evidently._pydantic_compat import BaseModel
from evidently.legacy.core import new_id
from evidently.sdk.artifacts import Artifact
from evidently.sdk.artifacts import ArtifactID
from evidently.sdk.artifacts import ArtifactVersion
from evidently.sdk.artifacts import ArtifactVersionID
from evidently.sdk.artifacts import VersionOrLatest
from evidently.ui.service.errors import ArtifactNotFound
from evidently.ui.service.storage.artifacts import ArtifactStorage
from evidently.ui.service.storage.fslocation import FSLocation
from evidently.ui.service.type_aliases import ProjectID

ARTIFACTS_DIR = "artifacts"
VERSIONS_DIR = "versions"


class ArtifactStorageState(BaseModel):
    artifacts: Dict[ArtifactID, Artifact] = {}
    versions: Dict[ArtifactVersionID, ArtifactVersion] = {}


class FileArtifactStorage(ArtifactStorage):
    base_path: str
    _location: Optional[FSLocation] = None

    def __init__(self, base_path: str):
        self.base_path = base_path
        super().__init__(base_path=base_path)

    @property
    def location(self) -> FSLocation:
        if self._location is None:
            self._location = FSLocation(self.base_path)
        return self._location

    def _get_artifact_metadata_path(self, project_id: ProjectID, artifact_id: ArtifactID) -> str:
        return posixpath.join(str(project_id), ARTIFACTS_DIR, str(artifact_id), "metadata.json")

    def _get_version_path(self, project_id: ProjectID, artifact_id: ArtifactID, version_id: ArtifactVersionID) -> str:
        return posixpath.join(str(project_id), ARTIFACTS_DIR, str(artifact_id), VERSIONS_DIR, f"{version_id}.json")

    async def list_artifacts(self, project_id: ProjectID) -> List[Artifact]:
        artifacts_dir = posixpath.join(str(project_id), ARTIFACTS_DIR)
        if not self.location.exists(artifacts_dir):
            return []
        artifacts = []
        for item in self.location.listdir(artifacts_dir):
            artifact_dir = posixpath.join(artifacts_dir, item)
            if self.location.isdir(artifact_dir):
                try:
                    artifact_id = ArtifactID(item)
                    artifact = await self.get_artifact(artifact_id)
                    if artifact and artifact.project_id == project_id:
                        artifacts.append(artifact)
                except (ValueError, json.JSONDecodeError):
                    continue
        return artifacts

    async def get_artifact(self, artifact_id: ArtifactID) -> Optional[Artifact]:
        # Try to find in any project
        # This is a simplified version - in production you might want to store a mapping
        for project_dir in self.location.listdir(""):
            if self.location.isdir(project_dir):
                try:
                    path = self._get_artifact_metadata_path(ProjectID(project_dir), artifact_id)
                    if self.location.exists(path):
                        with self.location.open(path, "r") as f:
                            data = json.load(f)
                            return Artifact(**data)
                except (ValueError, json.JSONDecodeError):
                    continue
        return None

    async def get_artifact_by_name(self, project_id: ProjectID, name: str) -> Optional[Artifact]:
        artifacts = await self.list_artifacts(project_id)
        return next((a for a in artifacts if a.name == name), None)

    async def add_artifact(self, project_id: ProjectID, artifact: Artifact) -> Artifact:
        artifact.id = new_id()
        artifact.project_id = project_id
        path = self._get_artifact_metadata_path(project_id, artifact.id)
        self.location.makedirs(posixpath.dirname(path))
        with self.location.open(path, "w") as f:
            json.dump(artifact.dict(), f, indent=2, default=str)
        return artifact

    async def delete_artifact(self, artifact_id: ArtifactID) -> None:
        artifact = await self.get_artifact(artifact_id)
        if artifact:
            # Delete the entire artifact directory (includes metadata.json and versions/)
            artifact_dir = posixpath.join(str(artifact.project_id), ARTIFACTS_DIR, str(artifact_id))
            if self.location.exists(artifact_dir):
                self.location.rmtree(artifact_dir)

    async def update_artifact(self, artifact_id: ArtifactID, artifact: Artifact) -> None:
        existing = await self.get_artifact(artifact_id)
        if not existing:
            raise ArtifactNotFound()
        path = self._get_artifact_metadata_path(artifact.project_id, artifact_id)
        with self.location.open(path, "w") as f:
            json.dump(artifact.dict(), f, indent=2, default=str)

    async def list_artifact_versions(self, artifact_id: ArtifactID) -> List[ArtifactVersion]:
        artifact = await self.get_artifact(artifact_id)
        if not artifact:
            return []
        versions_dir = posixpath.join(str(artifact.project_id), ARTIFACTS_DIR, str(artifact_id), VERSIONS_DIR)
        if not self.location.exists(versions_dir):
            return []
        versions = []
        for filename in self.location.listdir(versions_dir):
            if filename.endswith(".json"):
                version_id = ArtifactVersionID(filename[:-5])
                version = await self.get_artifact_version(version_id)
                if version:
                    versions.append(version)
        return sorted(versions, key=lambda v: v.version)

    async def get_artifact_version(self, artifact_version_id: ArtifactVersionID) -> Optional[ArtifactVersion]:
        # Find version in any project/artifact
        for project_dir in self.location.listdir(""):
            if self.location.isdir(project_dir):
                artifacts_dir = posixpath.join(project_dir, ARTIFACTS_DIR)
                if self.location.exists(artifacts_dir):
                    for artifact_dir in self.location.listdir(artifacts_dir):
                        versions_dir = posixpath.join(artifacts_dir, artifact_dir, VERSIONS_DIR)
                        if self.location.exists(versions_dir):
                            path = posixpath.join(versions_dir, f"{artifact_version_id}.json")
                            if self.location.exists(path):
                                with self.location.open(path, "r") as f:
                                    data = json.load(f)
                                    return ArtifactVersion(**data)
        return None

    async def get_artifact_version_by_version(
        self, artifact_id: ArtifactID, version: VersionOrLatest
    ) -> Optional[ArtifactVersion]:
        versions = await self.list_artifact_versions(artifact_id)
        if not versions:
            return None
        if isinstance(version, str) and version == "latest":
            return max(versions, key=lambda v: v.version)
        return next((v for v in versions if v.version == version), None)

    async def add_artifact_version(self, artifact_id: ArtifactID, artifact_version: ArtifactVersion) -> ArtifactVersion:
        artifact = await self.get_artifact(artifact_id)
        if not artifact:
            raise ArtifactNotFound()
        artifact_version.id = new_id()
        artifact_version.artifact_id = artifact_id
        path = self._get_version_path(artifact.project_id, artifact_id, artifact_version.id)
        self.location.makedirs(posixpath.dirname(path))
        with self.location.open(path, "w") as f:
            json.dump(artifact_version.dict(), f, indent=2, default=str)
        return artifact_version

    async def delete_artifact_version(self, artifact_version_id: ArtifactVersionID) -> None:
        version = await self.get_artifact_version(artifact_version_id)
        if version:
            artifact = await self.get_artifact(version.artifact_id)
            if artifact:
                path = self._get_version_path(artifact.project_id, version.artifact_id, artifact_version_id)
                if self.location.exists(path):
                    self.location.rmtree(path)
