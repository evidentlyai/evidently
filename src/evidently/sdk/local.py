"""
Local SDK managers that work directly with storage without requiring a service.

These managers provide the same SDK interface as RemoteWorkspace but work
directly with local storage, similar to how datasets work in Workspace.
"""

from typing import Any
from typing import List

from evidently.core.datasets import Descriptor
from evidently.errors import EvidentlyError
from evidently.legacy.core import new_id
from evidently.legacy.utils.sync import async_to_sync
from evidently.llm.prompts.content import ArtifactPromptContent
from evidently.llm.prompts.content import PromptContent
from evidently.sdk.artifacts import Artifact
from evidently.sdk.artifacts import ArtifactAPI
from evidently.sdk.artifacts import ArtifactID
from evidently.sdk.artifacts import ArtifactIDInput
from evidently.sdk.artifacts import ArtifactMetadata
from evidently.sdk.artifacts import ArtifactVersion
from evidently.sdk.artifacts import ArtifactVersionID
from evidently.sdk.artifacts import ArtifactVersionIDInput
from evidently.sdk.artifacts import ArtifactVersionMetadata
from evidently.sdk.artifacts import RemoteArtifact
from evidently.sdk.artifacts import VersionOrLatest
from evidently.sdk.configs import ConfigAPI
from evidently.sdk.configs import ConfigMetadata
from evidently.sdk.configs import ConfigVersion
from evidently.sdk.configs import ConfigVersionMetadata
from evidently.sdk.configs import GenericConfig
from evidently.sdk.configs import RemoteGenericConfig
from evidently.sdk.prompts import Prompt
from evidently.sdk.prompts import PromptAPI
from evidently.sdk.prompts import PromptMetadata
from evidently.sdk.prompts import PromptVersion
from evidently.sdk.prompts import PromptVersionMetadata
from evidently.sdk.prompts import RemotePrompt
from evidently.ui.service.storage.artifacts import ArtifactStorage
from evidently.ui.service.type_aliases import STR_UUID
from evidently.ui.service.type_aliases import ZERO_UUID
from evidently.ui.service.type_aliases import ProjectID
from evidently.ui.service.type_aliases import UserID


class LocalArtifactAPI(ArtifactAPI):
    """Local artifact manager that works directly with storage."""

    def __init__(self, artifact_storage: ArtifactStorage, user_id: UserID = ZERO_UUID):
        self._storage = artifact_storage
        self._user_id = user_id

    def list_artifacts(self, project_id: STR_UUID) -> List[RemoteArtifact]:
        """List all artifacts in a project."""
        project_uuid = ProjectID(project_id) if isinstance(project_id, str) else project_id
        artifacts = async_to_sync(self._storage.list_artifacts(project_uuid))
        return [self._to_remote_artifact(a) for a in artifacts]

    def get_or_create_artifact(self, project_id: STR_UUID, name: str) -> RemoteArtifact:
        """Get or create an artifact by name."""
        project_uuid = ProjectID(project_id) if isinstance(project_id, str) else project_id
        artifact = async_to_sync(self._storage.get_artifact_by_name(project_uuid, name))
        if artifact is None:
            artifact = Artifact(
                id=new_id(),
                project_id=project_uuid,
                name=name,
                metadata=ArtifactMetadata(),
            )
            artifact = async_to_sync(self._storage.add_artifact(project_uuid, artifact))
        return self._to_remote_artifact(artifact)

    def get_artifact(self, project_id: STR_UUID, name: str) -> RemoteArtifact:
        """Get an artifact by name."""
        project_uuid = ProjectID(project_id) if isinstance(project_id, str) else project_id
        artifact = async_to_sync(self._storage.get_artifact_by_name(project_uuid, name))
        if artifact is None:
            raise EvidentlyError("artifact not found")
        return self._to_remote_artifact(artifact)

    def get_artifact_by_id(self, project_id: STR_UUID, artifact_id: STR_UUID) -> RemoteArtifact:
        """Get an artifact by ID."""
        artifact_uuid = ArtifactID(artifact_id) if isinstance(artifact_id, str) else artifact_id
        artifact = async_to_sync(self._storage.get_artifact(artifact_uuid))
        if artifact is None:
            raise EvidentlyError("artifact not found")
        return self._to_remote_artifact(artifact)

    def create_artifact(self, project_id: STR_UUID, name: str) -> RemoteArtifact:
        """Create a new artifact."""
        project_uuid = ProjectID(project_id) if isinstance(project_id, str) else project_id
        artifact = Artifact(
            id=new_id(),
            project_id=project_uuid,
            name=name,
            metadata=ArtifactMetadata(),
        )
        artifact = async_to_sync(self._storage.add_artifact(project_uuid, artifact))
        return self._to_remote_artifact(artifact)

    def delete_artifact(self, artifact_id: ArtifactIDInput):
        """Delete an artifact."""
        artifact_id_uuid = ArtifactID(artifact_id) if isinstance(artifact_id, str) else artifact_id
        async_to_sync(self._storage.delete_artifact(artifact_id_uuid))

    def update_artifact(self, artifact: Artifact):
        """Update an artifact."""
        async_to_sync(self._storage.update_artifact(artifact.id, artifact))

    def list_versions(self, artifact_id: ArtifactIDInput) -> List[ArtifactVersion]:
        """List all versions of an artifact."""
        artifact_id_uuid = ArtifactID(artifact_id) if isinstance(artifact_id, str) else artifact_id
        return async_to_sync(self._storage.list_artifact_versions(artifact_id_uuid))

    def get_version(self, artifact_id: ArtifactIDInput, version: VersionOrLatest = "latest") -> ArtifactVersion:
        """Get a specific version of an artifact."""
        artifact_id_uuid = ArtifactID(artifact_id) if isinstance(artifact_id, str) else artifact_id
        artifact_version = async_to_sync(self._storage.get_artifact_version_by_version(artifact_id_uuid, version))
        if artifact_version is None:
            raise EvidentlyError("artifact version not found")
        return artifact_version

    def get_version_by_id(self, artifact_version_id: ArtifactVersionIDInput) -> ArtifactVersion:
        """Get a version by its ID."""
        version_id_uuid = (
            ArtifactVersionID(artifact_version_id) if isinstance(artifact_version_id, str) else artifact_version_id
        )
        version = async_to_sync(self._storage.get_artifact_version(version_id_uuid))
        if version is None:
            raise EvidentlyError("artifact version not found")
        return version

    def create_version(self, artifact_id: ArtifactIDInput, version: int, content: Any) -> ArtifactVersion:
        """Create a new version of an artifact."""
        artifact_id_uuid = ArtifactID(artifact_id) if isinstance(artifact_id, str) else artifact_id
        artifact_version = ArtifactVersion(
            id=new_id(),
            artifact_id=artifact_id_uuid,
            version=version,
            content=content,
            metadata=ArtifactVersionMetadata(),
        )
        return async_to_sync(self._storage.add_artifact_version(artifact_id_uuid, artifact_version))

    def delete_version(self, artifact_version_id: ArtifactVersionIDInput):
        """Delete a version."""
        version_id_uuid = (
            ArtifactVersionID(artifact_version_id) if isinstance(artifact_version_id, str) else artifact_version_id
        )
        async_to_sync(self._storage.delete_artifact_version(version_id_uuid))

    def bump_artifact_version(self, artifact_id: ArtifactIDInput, content: Any) -> ArtifactVersion:
        """Bump artifact version (create next version)."""
        try:
            latest = self.get_version(artifact_id)
            version = latest.version + 1
        except EvidentlyError as e:
            if e.get_message() != "EvidentlyError: artifact version not found":
                raise e
            version = 1
        return self.create_version(artifact_id, version, content)

    def _to_remote_artifact(self, artifact: Artifact) -> RemoteArtifact:
        """Convert Artifact to RemoteArtifact."""
        return RemoteArtifact(**artifact.dict()).bind(self)


class LocalPromptAPI(PromptAPI):
    """Local prompt API that works with artifacts storage via ArtifactPromptContent."""

    def __init__(self, artifact_storage: ArtifactStorage, user_id: UserID = ZERO_UUID):
        self._artifact_manager = LocalArtifactAPI(artifact_storage, user_id)
        self._storage = artifact_storage
        self._user_id = user_id

    def _artifact_to_prompt(self, artifact: RemoteArtifact) -> RemotePrompt:
        """Convert artifact to prompt."""
        prompt = Prompt(
            id=artifact.id,
            project_id=artifact.project_id,
            name=artifact.name,
            metadata=PromptMetadata(
                created_at=artifact.metadata.created_at,
                updated_at=artifact.metadata.updated_at,
                author=artifact.metadata.author,
            ),
        )
        return RemotePrompt(**prompt.dict()).bind(self)

    def _artifact_version_to_prompt_version(self, artifact_version: ArtifactVersion) -> PromptVersion:
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

    def list_prompts(self, project_id: STR_UUID) -> List[RemotePrompt]:
        """List all prompts in a project."""
        artifacts = self._artifact_manager.list_artifacts(project_id)
        return [self._artifact_to_prompt(a) for a in artifacts]

    def get_or_create_prompt(self, project_id: STR_UUID, name: str) -> RemotePrompt:
        """Get or create a prompt by name."""
        try:
            return self.get_prompt(project_id, name)
        except EvidentlyError as e:
            if not e.get_message() == "EvidentlyError: artifact not found":
                raise e
            return self.create_prompt(project_id, name)

    def get_prompt(self, project_id: STR_UUID, name: str) -> RemotePrompt:
        """Get a prompt by name."""
        artifact = self._artifact_manager.get_artifact(project_id, name)
        return self._artifact_to_prompt(artifact)

    def get_prompt_by_id(self, project_id: STR_UUID, prompt_id: STR_UUID) -> RemotePrompt:
        """Get a prompt by ID."""
        artifact = self._artifact_manager.get_artifact_by_id(project_id, prompt_id)
        return self._artifact_to_prompt(artifact)

    def create_prompt(self, project_id: STR_UUID, name: str) -> RemotePrompt:
        """Create a new prompt."""
        artifact = self._artifact_manager.create_artifact(project_id, name)
        return self._artifact_to_prompt(artifact)

    def delete_prompt(self, prompt_id: STR_UUID):
        """Delete a prompt."""
        artifact_uuid = ArtifactID(prompt_id) if isinstance(prompt_id, str) else prompt_id
        return self._artifact_manager.delete_artifact(artifact_uuid)

    def update_prompt(self, prompt: Prompt):
        """Update a prompt."""
        artifact = Artifact(
            id=prompt.id,
            project_id=prompt.project_id,
            name=prompt.name,
            metadata=ArtifactMetadata(
                created_at=prompt.metadata.created_at,
                updated_at=prompt.metadata.updated_at,
                author=prompt.metadata.author,
            ),
        )
        return self._artifact_manager.update_artifact(artifact)

    def list_versions(self, prompt_id: STR_UUID) -> List[PromptVersion]:
        """List all versions of a prompt."""
        artifact_uuid = ArtifactID(prompt_id) if isinstance(prompt_id, str) else prompt_id
        artifact_versions = self._artifact_manager.list_versions(artifact_uuid)
        return [self._artifact_version_to_prompt_version(av) for av in artifact_versions]

    def get_version(self, prompt_id: STR_UUID, version: VersionOrLatest = "latest") -> PromptVersion:
        """Get a specific version of a prompt."""
        artifact_uuid = ArtifactID(prompt_id) if isinstance(prompt_id, str) else prompt_id
        artifact_version = self._artifact_manager.get_version(artifact_uuid, version)
        return self._artifact_version_to_prompt_version(artifact_version)

    def get_version_by_id(self, prompt_version_id: STR_UUID) -> PromptVersion:
        """Get a version by its ID."""
        version_uuid = ArtifactVersionID(prompt_version_id) if isinstance(prompt_version_id, str) else prompt_version_id
        artifact_version = self._artifact_manager.get_version_by_id(version_uuid)
        return self._artifact_version_to_prompt_version(artifact_version)

    def create_version(self, prompt_id: STR_UUID, version: int, content: Any) -> PromptVersion:
        """Create a new version of a prompt."""
        artifact_uuid = ArtifactID(prompt_id) if isinstance(prompt_id, str) else prompt_id
        # Wrap PromptContent in ArtifactPromptContent
        if not isinstance(content, PromptContent):
            content = PromptContent.parse(content)
        artifact_content = ArtifactPromptContent.from_value(content)

        artifact_version = self._artifact_manager.create_version(artifact_uuid, version, artifact_content)
        return self._artifact_version_to_prompt_version(artifact_version)

    def delete_version(self, prompt_version_id: STR_UUID):
        """Delete a version."""
        version_uuid = ArtifactVersionID(prompt_version_id) if isinstance(prompt_version_id, str) else prompt_version_id
        return self._artifact_manager.delete_version(version_uuid)

    def bump_prompt_version(self, prompt_id: STR_UUID, content: Any) -> PromptVersion:
        """Bump prompt version (create next version)."""
        artifact_uuid = ArtifactID(prompt_id) if isinstance(prompt_id, str) else prompt_id
        # Wrap PromptContent in ArtifactPromptContent
        if not isinstance(content, PromptContent):
            content = PromptContent.parse(content)
        artifact_content = ArtifactPromptContent.from_value(content)

        artifact_version = self._artifact_manager.bump_artifact_version(artifact_uuid, artifact_content)
        return self._artifact_version_to_prompt_version(artifact_version)


class LocalConfigAPI(ConfigAPI):
    """Local config API that works with artifacts storage."""

    def __init__(self, artifact_storage: ArtifactStorage, user_id: UserID = ZERO_UUID):
        self._artifact_manager = LocalArtifactAPI(artifact_storage, user_id)
        self._storage = artifact_storage
        self._user_id = user_id

    def _artifact_to_config(self, artifact: RemoteArtifact) -> RemoteGenericConfig:
        """Convert artifact to config."""
        config = GenericConfig(
            id=artifact.id,
            project_id=artifact.project_id,
            name=artifact.name,
            metadata=ConfigMetadata(
                created_at=artifact.metadata.created_at,
                updated_at=artifact.metadata.updated_at,
                author=artifact.metadata.author,
                description=artifact.metadata.description,
            ),
        )
        return RemoteGenericConfig(**config.dict()).bind(self)

    def _artifact_version_to_config_version(self, artifact_version: ArtifactVersion) -> ConfigVersion:
        """Convert artifact version to config version."""
        return ConfigVersion(
            id=artifact_version.id,
            artifact_id=artifact_version.artifact_id,
            version=artifact_version.version,
            content=artifact_version.content,
            metadata=ConfigVersionMetadata(
                created_at=artifact_version.metadata.created_at,
                updated_at=artifact_version.metadata.updated_at,
                author=artifact_version.metadata.author,
                comment=artifact_version.metadata.comment,
            ),
        )

    def list_configs(self, project_id: STR_UUID) -> List[RemoteGenericConfig]:
        """List all configs in a project."""
        artifacts = self._artifact_manager.list_artifacts(project_id)
        return [self._artifact_to_config(a) for a in artifacts]

    def get_or_create_config(self, project_id: STR_UUID, name: str) -> RemoteGenericConfig:
        """Get or create a config by name."""
        artifact = self._artifact_manager.get_or_create_artifact(project_id, name)
        return self._artifact_to_config(artifact)

    def get_config(self, project_id: STR_UUID, name: str) -> RemoteGenericConfig:
        """Get a config by name."""
        artifact = self._artifact_manager.get_artifact(project_id, name)
        return self._artifact_to_config(artifact)

    def get_config_by_id(self, project_id: STR_UUID, config_id: STR_UUID) -> RemoteGenericConfig:
        """Get a config by ID."""
        artifact = self._artifact_manager.get_artifact_by_id(project_id, config_id)
        return self._artifact_to_config(artifact)

    def create_config(self, project_id: STR_UUID, name: str) -> RemoteGenericConfig:
        """Create a new config."""
        artifact = self._artifact_manager.create_artifact(project_id, name)
        return self._artifact_to_config(artifact)

    def delete_config(self, config_id: STR_UUID):
        """Delete a config."""
        artifact_uuid = ArtifactID(config_id) if isinstance(config_id, str) else config_id
        return self._artifact_manager.delete_artifact(artifact_uuid)

    def update_config(self, config: GenericConfig):
        """Update a config."""
        artifact = Artifact(
            id=config.id,
            project_id=config.project_id,
            name=config.name,
            metadata=ArtifactMetadata(
                created_at=config.metadata.created_at,
                updated_at=config.metadata.updated_at,
                author=config.metadata.author,
                description=config.metadata.description,
            ),
        )
        return self._artifact_manager.update_artifact(artifact)

    def list_versions(self, config_id: STR_UUID) -> List[ConfigVersion]:
        """List all versions of a config."""
        artifact_uuid = ArtifactID(config_id) if isinstance(config_id, str) else config_id
        artifact_versions = self._artifact_manager.list_versions(artifact_uuid)
        return [self._artifact_version_to_config_version(av) for av in artifact_versions]

    def get_version(self, config_id: STR_UUID, version: VersionOrLatest = "latest") -> ConfigVersion:
        """Get a specific version of a config."""
        artifact_uuid = ArtifactID(config_id) if isinstance(config_id, str) else config_id
        artifact_version = self._artifact_manager.get_version(artifact_uuid, version)
        return self._artifact_version_to_config_version(artifact_version)

    def get_version_by_id(self, config_version_id: STR_UUID) -> ConfigVersion:
        """Get a version by its ID."""
        version_uuid = ArtifactVersionID(config_version_id) if isinstance(config_version_id, str) else config_version_id
        artifact_version = self._artifact_manager.get_version_by_id(version_uuid)
        return self._artifact_version_to_config_version(artifact_version)

    def create_version(self, config_id: STR_UUID, version: int, content: Any) -> ConfigVersion:
        """Create a new version of a config."""
        artifact_uuid = ArtifactID(config_id) if isinstance(config_id, str) else config_id
        artifact_version = self._artifact_manager.create_version(artifact_uuid, version, content)
        return self._artifact_version_to_config_version(artifact_version)

    def delete_version(self, config_version_id: STR_UUID):
        """Delete a version."""
        version_uuid = ArtifactVersionID(config_version_id) if isinstance(config_version_id, str) else config_version_id
        return self._artifact_manager.delete_version(version_uuid)

    def bump_config_version(self, config_id: STR_UUID, content: Any) -> ConfigVersion:
        """Bump config version (create next version)."""
        artifact_uuid = ArtifactID(config_id) if isinstance(config_id, str) else config_id
        artifact_version = self._artifact_manager.bump_artifact_version(artifact_uuid, content)
        return self._artifact_version_to_config_version(artifact_version)

    def _add_typed_version(self, project_id: STR_UUID, name: str, value: Any) -> ConfigVersion:
        """Add a typed version to a config."""
        config = self.get_or_create_config(project_id, name)
        return self.bump_config_version(config.id, value)

    def _get_typed_version(self, project_id: STR_UUID, name: str, version: VersionOrLatest, type_) -> Any:
        """Get a typed version from a config."""
        config = self.get_config(project_id, name)
        config_version = self.get_version(config.id, version)
        value = config_version.content.get_value()
        if not isinstance(value, type_):
            raise ValueError(f"Config with name '{name}' is not a {type_.__class__.__name__}")
        return value

    def add_descriptor(self, project_id: STR_UUID, name: str, descriptor: Descriptor):
        """Add a descriptor to a config."""
        return self._add_typed_version(project_id, name, descriptor)

    def get_descriptor(self, project_id: STR_UUID, name: str, version: VersionOrLatest = "latest") -> Descriptor:
        """Get a descriptor from a config."""
        return self._get_typed_version(project_id, name, version, Descriptor)  # type: ignore[type-abstract]
