"""
Backward-compatible configs SDK that uses artifacts implementation.

This module re-exports artifacts as configs for backward compatibility.
All config classes are now aliases to artifact classes.
"""

import json
from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING
from typing import Any
from typing import ClassVar
from typing import List
from typing import Type
from typing import TypeVar

from evidently._pydantic_compat import Field
from evidently._pydantic_compat import PrivateAttr
from evidently.core.datasets import Descriptor
from evidently.errors import EvidentlyError
from evidently.sdk.artifacts import Artifact as GenericConfig
from evidently.sdk.artifacts import ArtifactContent as ConfigContent
from evidently.sdk.artifacts import ArtifactContentType as ConfigContentType
from evidently.sdk.artifacts import ArtifactID
from evidently.sdk.artifacts import ArtifactIDInput as ConfigIDInput
from evidently.sdk.artifacts import ArtifactMetadata as ConfigMetadata
from evidently.sdk.artifacts import ArtifactVersion as ConfigVersion
from evidently.sdk.artifacts import ArtifactVersionID as ConfigVersionID
from evidently.sdk.artifacts import ArtifactVersionIDInput as ConfigVersionIDInput
from evidently.sdk.artifacts import ArtifactVersionMetadata as ConfigVersionMetadata
from evidently.sdk.artifacts import VersionOrLatest
from evidently.ui.service.type_aliases import STR_UUID
from evidently.ui.service.type_aliases import ZERO_UUID
from evidently.ui.service.type_aliases import ProjectID

if TYPE_CHECKING:
    from evidently.ui.workspace import CloudWorkspace

T = TypeVar("T")


class RemoteGenericConfig(GenericConfig):
    """Remote config that binds to ConfigAPI.

    Provides methods to interact with a remote config through the API,
    including version management and updates. Use `ConfigAPI` to create
    and manage remote configs.
    """

    _api: "ConfigAPI" = PrivateAttr()

    id: ArtifactID = ZERO_UUID
    """Unique config identifier."""
    project_id: ProjectID = ZERO_UUID
    """Project this config belongs to."""
    name: str
    """Name of the config."""
    metadata: ConfigMetadata = Field(default_factory=ConfigMetadata)
    """Metadata about the config."""

    def bind(self, api: "ConfigAPI") -> "RemoteGenericConfig":
        """Bind this config to an API instance.

        Args:
        * `api`: `ConfigAPI` to use for operations.

        Returns:
        * Self for method chaining.
        """
        self._api = api
        return self

    def list_versions(self) -> List[ConfigVersion]:
        """List all versions of this config.

        Returns:
        * List of `ConfigVersion` objects.
        """
        return self._api.list_versions(self.id)

    def get_version(self, version: VersionOrLatest = "latest") -> ConfigVersion:
        """Get a specific version of this config.

        Args:
        * `version`: Version number or `"latest"`.

        Returns:
        * `ConfigVersion` for the specified version.
        """
        return self._api.get_version(self.id, version)

    def bump_version(self, content: Any):
        """Create a new version with the given content.

        Args:
        * `content`: Content to store in the new version.

        Returns:
        * New `ConfigVersion` with incremented version number.
        """
        return self._api.bump_config_version(self.id, content)

    def delete(self):
        """Delete this config and all its versions.

        This operation is irreversible and will permanently remove the config
        and all associated versions from the workspace.
        """
        return self._api.delete_config(self.id)

    def delete_version(self, version_id: ConfigVersionID):
        """Delete a specific version.

        This operation is irreversible and will permanently remove the version.

        Args:
        * `version_id`: ID of the version to delete.
        """
        return self._api.delete_version(version_id)

    def save(self):
        """Save changes to this config's metadata to the remote workspace.

        Updates the config's name and metadata fields. Does not affect versions.
        """
        self._api.update_config(self)


class DescriptorContent(ConfigContent[Descriptor]):
    """Backward-compatible DescriptorContent."""

    __value_class__: ClassVar = Descriptor
    __value_type__: ClassVar = ConfigContentType.Descriptor

    @classmethod
    def from_value(cls, value: Descriptor) -> "ConfigContent":
        return DescriptorContent(data=json.loads(value.json()))


class ConfigAPI(ABC):
    """Abstract base class for config API."""

    @abstractmethod
    def list_configs(self, project_id: STR_UUID) -> List[RemoteGenericConfig]:
        """List all configs in a project."""
        ...

    @abstractmethod
    def get_or_create_config(self, project_id: STR_UUID, name: str) -> RemoteGenericConfig:
        """Get or create a config by name."""
        ...

    @abstractmethod
    def get_config(self, project_id: STR_UUID, name: str) -> RemoteGenericConfig:
        """Get a config by name."""
        ...

    @abstractmethod
    def get_config_by_id(self, project_id: STR_UUID, config_id: ConfigIDInput) -> RemoteGenericConfig:
        """Get a config by ID."""
        ...

    @abstractmethod
    def create_config(self, project_id: STR_UUID, name: str) -> RemoteGenericConfig:
        """Create a new config."""
        ...

    @abstractmethod
    def delete_config(self, config_id: ConfigIDInput):
        """Delete a config."""
        ...

    @abstractmethod
    def update_config(self, config: GenericConfig):
        """Update a config."""
        ...

    @abstractmethod
    def list_versions(self, config_id: ConfigIDInput) -> List[ConfigVersion]:
        """List all versions of a config."""
        ...

    @abstractmethod
    def get_version(self, config_id: ConfigIDInput, version: VersionOrLatest = "latest") -> ConfigVersion:
        """Get a specific version of a config."""
        ...

    @abstractmethod
    def get_version_by_id(self, config_version_id: ConfigVersionIDInput) -> ConfigVersion:
        """Get a version by its ID."""
        ...

    @abstractmethod
    def create_version(self, config_id: ConfigIDInput, version: int, content: Any) -> ConfigVersion:
        """Create a new version of a config."""
        ...

    @abstractmethod
    def delete_version(self, config_version_id: ConfigVersionIDInput):
        """Delete a version."""
        ...

    @abstractmethod
    def bump_config_version(self, config_id: ConfigIDInput, content: Any) -> ConfigVersion:
        """Bump config version (create next version)."""
        ...


class CloudConfigAPI(ConfigAPI):
    """Cloud-only config API that works with /api/configs endpoint.

    Uses backported Config models (which are actually Artifact models).
    Requires a `CloudWorkspace` instance.
    """

    def __init__(self, workspace: "CloudWorkspace"):
        """Initialize the API.

        Args:
        * `workspace`: `CloudWorkspace` to use for API calls.
        """
        self._ws = workspace

    def list_configs(self, project_id: STR_UUID) -> List[RemoteGenericConfig]:
        return [
            p.bind(self)
            for p in self._ws._request(
                "/api/configs",
                "GET",
                query_params={"project_id": str(project_id)},
                response_model=List[RemoteGenericConfig],
            )
        ]

    def get_or_create_config(self, project_id: STR_UUID, name: str) -> RemoteGenericConfig:
        try:
            return self.get_config(project_id, name)
        except EvidentlyError as e:
            if not e.get_message() == "EvidentlyError: config not found":
                raise e
            return self.create_config(project_id, name)

    def get_config(self, project_id: STR_UUID, name: str) -> RemoteGenericConfig:
        return self._ws._request(
            f"/api/configs/by-name/{name}",
            "GET",
            query_params={"project_id": str(project_id)},
            response_model=RemoteGenericConfig,
        ).bind(self)

    def get_config_by_id(self, project_id: STR_UUID, config_id: ConfigIDInput) -> RemoteGenericConfig:
        return self._ws._request(f"/api/configs/{config_id}", "GET", response_model=RemoteGenericConfig).bind(self)

    def create_config(self, project_id: STR_UUID, name: str) -> RemoteGenericConfig:
        return self._ws._request(
            "/api/configs/",
            "POST",
            query_params={"project_id": str(project_id)},
            body=GenericConfig(name=name, metadata=ConfigMetadata()).dict(),
            response_model=RemoteGenericConfig,
        ).bind(self)

    def delete_config(self, config_id: ConfigIDInput):
        return self._ws._request(f"/api/configs/{config_id}", "DELETE")

    def update_config(self, config: GenericConfig):
        self._ws._request(
            f"/api/configs/{config.id}",
            "PUT",
            body=json.loads(config.json()),
        )

    def list_versions(self, config_id: ConfigIDInput) -> List[ConfigVersion]:
        return self._ws._request(f"/api/configs/{config_id}/versions", "GET", response_model=List[ConfigVersion])

    def get_version(self, config_id: ConfigIDInput, version: VersionOrLatest = "latest") -> ConfigVersion:
        return self._ws._request(f"/api/configs/{config_id}/versions/{version}", "GET", response_model=ConfigVersion)

    def get_version_by_id(self, config_version_id: ConfigVersionIDInput) -> ConfigVersion:
        return self._ws._request(
            f"/api/configs/config-versions/{config_version_id}", "GET", response_model=ConfigVersion
        )

    def create_version(self, config_id: ConfigIDInput, version: int, content: Any) -> ConfigVersion:
        return self._ws._request(
            f"/api/configs/{config_id}/versions",
            "POST",
            body=ConfigVersion(version=version, content=content).dict(),
            response_model=ConfigVersion,
        )

    def delete_version(self, config_version_id: ConfigVersionIDInput):
        self._ws._request(f"/api/configs/config-versions/{config_version_id}", "DELETE")

    def bump_config_version(self, config_id: ConfigIDInput, content: Any) -> ConfigVersion:
        try:
            latest = self.get_version(config_id)
            version = latest.version + 1
        except EvidentlyError as e:
            if e.get_message() != "EvidentlyError: config version not found":
                raise e
            version = 1
        return self.create_version(config_id, version, content)

    def _add_typed_version(self, project_id: STR_UUID, name: str, value: Any) -> ConfigVersion:
        config = self.get_or_create_config(project_id, name)
        return self.bump_config_version(config.id, value)

    def _get_typed_version(self, project_id: STR_UUID, name: str, version: VersionOrLatest, type_: Type[T]) -> T:
        config = self.get_config(project_id, name)
        config_version = self.get_version(config.id, version)
        value = config_version.content.get_value()
        if not isinstance(value, type_):
            raise ValueError(f"Config with name '{name}' is not a {type_.__class__.__name__}")
        return value

    def add_descriptor(self, project_id: STR_UUID, name: str, descriptor: Descriptor):
        """Add or update a descriptor config.

        Args:
        * `project_id`: Project ID.
        * `name`: Name of the descriptor config.
        * `descriptor`: `Descriptor` object to store.

        Returns:
        * `ConfigVersion` containing the descriptor.
        """
        return self._add_typed_version(project_id, name, descriptor)

    def get_descriptor(self, project_id: STR_UUID, name: str, version: VersionOrLatest = "latest") -> Descriptor:
        """Get a descriptor config.

        Args:
        * `project_id`: Project ID.
        * `name`: Name of the descriptor config.
        * `version`: Version number or `"latest"`.

        Returns:
        * `Descriptor` object from the config.
        """
        return self._get_typed_version(project_id, name, version, Descriptor)  # type: ignore[type-abstract]


__all__ = [
    "ConfigMetadata",
    "ConfigVersionMetadata",
    "GenericConfig",
    "ConfigContent",
    "RemoteGenericConfig",
    "CloudConfigAPI",
    "ConfigVersion",
    "ConfigAPI",
]
