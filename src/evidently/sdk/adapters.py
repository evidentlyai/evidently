"""
Adapters that bridge between different SDK interfaces and API endpoints.

These adapters allow using one SDK interface while delegating to a different
underlying manager/API.
"""

from typing import TYPE_CHECKING
from typing import Any
from typing import List

from evidently.errors import EvidentlyError
from evidently.llm.prompts.content import ArtifactPromptContent
from evidently.llm.prompts.content import PromptContent
from evidently.sdk.artifacts import Artifact
from evidently.sdk.artifacts import ArtifactAPI
from evidently.sdk.artifacts import ArtifactMetadata
from evidently.sdk.artifacts import ArtifactVersion
from evidently.sdk.artifacts import ArtifactVersionMetadata
from evidently.sdk.artifacts import RemoteArtifact
from evidently.sdk.artifacts import RemoteArtifactAPI
from evidently.sdk.artifacts import VersionOrLatest
from evidently.sdk.configs import CloudConfigAPI
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
from evidently.ui.service.type_aliases import STR_UUID

if TYPE_CHECKING:
    from evidently.ui.workspace import CloudWorkspace
    from evidently.ui.workspace import RemoteWorkspace


class PromptArtifactAdapter(PromptAPI):
    """Adapter that implements PromptAPI interface but uses RemoteArtifactAPI.

    Allows using prompts SDK interface with OSS artifacts API.
    """

    def __init__(self, workspace: "RemoteWorkspace"):
        """Initialize the adapter.

        Args:
        * `workspace`: `RemoteWorkspace` to use for API calls.
        """
        self._api = RemoteArtifactAPI(workspace)
        self._ws = workspace

    def _artifact_to_prompt(self, artifact: RemoteArtifact) -> RemotePrompt:
        """Convert artifact to prompt.

        Args:
        * `artifact`: `RemoteArtifact` to convert.

        Returns:
        * `RemotePrompt` with data from the artifact.
        """
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
        artifacts = self._api.list_artifacts(project_id)
        return [self._artifact_to_prompt(a) for a in artifacts]

    def get_or_create_prompt(self, project_id: STR_UUID, name: str) -> RemotePrompt:
        try:
            return self.get_prompt(project_id, name)
        except EvidentlyError as e:
            error_msg = e.get_message()
            if "artifact not found" not in error_msg.lower() and "Artifact not found" not in error_msg:
                raise e
            return self.create_prompt(project_id, name)

    def get_prompt(self, project_id: STR_UUID, name: str) -> RemotePrompt:
        artifact = self._api.get_artifact(project_id, name)
        return self._artifact_to_prompt(artifact)

    def get_prompt_by_id(self, project_id: STR_UUID, prompt_id: STR_UUID) -> RemotePrompt:
        artifact = self._api.get_artifact_by_id(project_id, prompt_id)
        return self._artifact_to_prompt(artifact)

    def create_prompt(self, project_id: STR_UUID, name: str) -> RemotePrompt:
        artifact = self._api.create_artifact(project_id, name)
        return self._artifact_to_prompt(artifact)

    def delete_prompt(self, prompt_id: STR_UUID):
        return self._api.delete_artifact(prompt_id)

    def update_prompt(self, prompt: Prompt):
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
        return self._api.update_artifact(artifact)

    def list_versions(self, prompt_id: STR_UUID) -> List[PromptVersion]:
        artifact_versions = self._api.list_versions(prompt_id)
        return [self._artifact_version_to_prompt_version(av) for av in artifact_versions]

    def get_version(self, prompt_id: STR_UUID, version: VersionOrLatest = "latest") -> PromptVersion:
        artifact_version = self._api.get_version(prompt_id, version)
        return self._artifact_version_to_prompt_version(artifact_version)

    def get_version_by_id(self, prompt_version_id: STR_UUID) -> PromptVersion:
        artifact_version = self._api.get_version_by_id(prompt_version_id)
        return self._artifact_version_to_prompt_version(artifact_version)

    def create_version(self, prompt_id: STR_UUID, version: int, content: Any) -> PromptVersion:
        # Wrap PromptContent in ArtifactPromptContent
        if not isinstance(content, PromptContent):
            content = PromptContent.parse(content)
        artifact_content = ArtifactPromptContent.from_value(content)

        artifact_version = self._api.create_version(prompt_id, version, artifact_content)
        return self._artifact_version_to_prompt_version(artifact_version)

    def delete_version(self, prompt_version_id: STR_UUID):
        return self._api.delete_version(prompt_version_id)

    def bump_prompt_version(self, prompt_id: STR_UUID, content: Any) -> PromptVersion:
        # Wrap PromptContent in ArtifactPromptContent
        if not isinstance(content, PromptContent):
            content = PromptContent.parse(content)
        artifact_content = ArtifactPromptContent.from_value(content)

        artifact_version = self._api.bump_artifact_version(prompt_id, artifact_content)
        return self._artifact_version_to_prompt_version(artifact_version)


class ConfigArtifactAdapter(ConfigAPI):
    """Adapter that implements ConfigAPI interface but uses RemoteArtifactAPI.

    Allows using configs SDK interface with OSS artifacts API.
    """

    def __init__(self, workspace: "RemoteWorkspace"):
        """Initialize the adapter.

        Args:
        * `workspace`: `RemoteWorkspace` to use for API calls.
        """
        self._api = RemoteArtifactAPI(workspace)
        self._ws = workspace

    def _artifact_to_config(self, artifact: RemoteArtifact) -> RemoteGenericConfig:
        """Convert artifact to config.

        Args:
        * `artifact`: `RemoteArtifact` to convert.

        Returns:
        * `RemoteGenericConfig` with data from the artifact.
        """
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

    def list_configs(self, project_id: STR_UUID) -> List[RemoteGenericConfig]:
        artifacts = self._api.list_artifacts(project_id)
        return [self._artifact_to_config(a) for a in artifacts]

    def get_or_create_config(self, project_id: STR_UUID, name: str) -> RemoteGenericConfig:
        artifact = self._api.get_or_create_artifact(project_id, name)
        return self._artifact_to_config(artifact)

    def get_config(self, project_id: STR_UUID, name: str) -> RemoteGenericConfig:
        artifact = self._api.get_artifact(project_id, name)
        return self._artifact_to_config(artifact)

    def get_config_by_id(self, project_id: STR_UUID, config_id: STR_UUID) -> RemoteGenericConfig:
        artifact = self._api.get_artifact_by_id(project_id, config_id)
        return self._artifact_to_config(artifact)

    def create_config(self, project_id: STR_UUID, name: str) -> RemoteGenericConfig:
        artifact = self._api.create_artifact(project_id, name)
        return self._artifact_to_config(artifact)

    def delete_config(self, config_id: STR_UUID):
        return self._api.delete_artifact(config_id)

    def update_config(self, config: GenericConfig):
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
        return self._api.update_artifact(artifact)

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

    def list_versions(self, config_id: STR_UUID) -> List[ConfigVersion]:
        artifact_versions = self._api.list_versions(config_id)
        return [self._artifact_version_to_config_version(av) for av in artifact_versions]

    def get_version(self, config_id: STR_UUID, version: VersionOrLatest = "latest") -> ConfigVersion:
        artifact_version = self._api.get_version(config_id, version)
        return self._artifact_version_to_config_version(artifact_version)

    def get_version_by_id(self, config_version_id: STR_UUID) -> ConfigVersion:
        artifact_version = self._api.get_version_by_id(config_version_id)
        return self._artifact_version_to_config_version(artifact_version)

    def create_version(self, config_id: STR_UUID, version: int, content: Any) -> ConfigVersion:
        artifact_version = self._api.create_version(config_id, version, content)
        return self._artifact_version_to_config_version(artifact_version)

    def delete_version(self, config_version_id: STR_UUID):
        return self._api.delete_version(config_version_id)

    def bump_config_version(self, config_id: STR_UUID, content: Any) -> ConfigVersion:
        artifact_version = self._api.bump_artifact_version(config_id, content)
        return self._artifact_version_to_config_version(artifact_version)

    def _add_typed_version(self, project_id: STR_UUID, name: str, value: Any) -> ConfigVersion:
        artifact = self._api.get_or_create_artifact(project_id, name)
        config = self._artifact_to_config(artifact)
        return self.bump_config_version(config.id, value)

    def _get_typed_version(self, project_id: STR_UUID, name: str, version: VersionOrLatest, type_) -> Any:
        config = self.get_config(project_id, name)
        config_version = self.get_version(config.id, version)
        value = config_version.content.get_value()
        if not isinstance(value, type_):
            raise ValueError(f"Config with name '{name}' is not a {type_.__class__.__name__}")
        return value

    def add_descriptor(self, project_id: STR_UUID, name: str, descriptor):
        """Add or update a descriptor config.

        Args:
        * `project_id`: Project ID.
        * `name`: Name of the descriptor config.
        * `descriptor`: `Descriptor` object to store.

        Returns:
        * `ConfigVersion` containing the descriptor.
        """
        return self._add_typed_version(project_id, name, descriptor)

    def get_descriptor(self, project_id: STR_UUID, name: str, version: VersionOrLatest = "latest"):
        """Get a descriptor config.

        Args:
        * `project_id`: Project ID.
        * `name`: Name of the descriptor config.
        * `version`: Version number or `"latest"`.

        Returns:
        * `Descriptor` object from the config.
        """
        from evidently.core.datasets import Descriptor

        return self._get_typed_version(project_id, name, version, Descriptor)


class ArtifactConfigAdapter(ArtifactAPI):
    """Adapter that implements ArtifactAPI interface but uses CloudConfigAPI.

    Allows using artifacts SDK interface with cloud configs API.
    """

    def __init__(self, workspace: "CloudWorkspace"):
        """Initialize the adapter.

        Args:
        * `workspace`: `CloudWorkspace` to use for API calls.
        """
        self._api = CloudConfigAPI(workspace)
        self._ws = workspace

    def _config_to_artifact(self, config: RemoteGenericConfig) -> RemoteArtifact:
        """Convert config to artifact.

        Args:
        * `config`: `RemoteGenericConfig` to convert.

        Returns:
        * `RemoteArtifact` with data from the config.
        """
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
        return RemoteArtifact(**artifact.dict()).bind(self)

    def list_artifacts(self, project_id: STR_UUID) -> List[RemoteArtifact]:
        configs = self._api.list_configs(project_id)
        return [self._config_to_artifact(c) for c in configs]

    def get_or_create_artifact(self, project_id: STR_UUID, name: str) -> RemoteArtifact:
        config = self._api.get_or_create_config(project_id, name)
        return self._config_to_artifact(config)

    def get_artifact(self, project_id: STR_UUID, name: str) -> RemoteArtifact:
        config = self._api.get_config(project_id, name)
        return self._config_to_artifact(config)

    def get_artifact_by_id(self, project_id: STR_UUID, artifact_id: STR_UUID) -> RemoteArtifact:
        config = self._api.get_config_by_id(project_id, artifact_id)
        return self._config_to_artifact(config)

    def create_artifact(self, project_id: STR_UUID, name: str) -> RemoteArtifact:
        config = self._api.create_config(project_id, name)
        return self._config_to_artifact(config)

    def delete_artifact(self, artifact_id: STR_UUID):
        return self._api.delete_config(artifact_id)

    def update_artifact(self, artifact: Artifact):
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
        return self._api.update_config(config)

    def _config_version_to_artifact_version(self, config_version: ConfigVersion) -> ArtifactVersion:
        """Convert config version to artifact version."""
        return ArtifactVersion(
            id=config_version.id,
            artifact_id=config_version.artifact_id,
            version=config_version.version,
            content=config_version.content,
            metadata=ArtifactVersionMetadata(
                created_at=config_version.metadata.created_at,
                updated_at=config_version.metadata.updated_at,
                author=config_version.metadata.author,
                comment=config_version.metadata.comment,
            ),
        )

    def list_versions(self, artifact_id: STR_UUID) -> List[ArtifactVersion]:
        config_versions = self._api.list_versions(artifact_id)
        return [self._config_version_to_artifact_version(cv) for cv in config_versions]

    def get_version(self, artifact_id: STR_UUID, version: VersionOrLatest = "latest") -> ArtifactVersion:
        config_version = self._api.get_version(artifact_id, version)
        return self._config_version_to_artifact_version(config_version)

    def get_version_by_id(self, artifact_version_id: STR_UUID) -> ArtifactVersion:
        config_version = self._api.get_version_by_id(artifact_version_id)
        return self._config_version_to_artifact_version(config_version)

    def create_version(self, artifact_id: STR_UUID, version: int, content: Any) -> ArtifactVersion:
        config_version = self._api.create_version(artifact_id, version, content)
        return self._config_version_to_artifact_version(config_version)

    def delete_version(self, artifact_version_id: STR_UUID):
        return self._api.delete_version(artifact_version_id)

    def bump_artifact_version(self, artifact_id: STR_UUID, content: Any) -> ArtifactVersion:
        config_version = self._api.bump_config_version(artifact_id, content)
        return self._config_version_to_artifact_version(config_version)
