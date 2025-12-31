import json
import uuid
from abc import ABC
from abc import abstractmethod
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING
from typing import Any
from typing import ClassVar
from typing import Dict
from typing import Generic
from typing import List
from typing import Literal
from typing import Optional
from typing import Type
from typing import TypeVar
from typing import Union

from evidently._pydantic_compat import BaseModel
from evidently._pydantic_compat import Field
from evidently._pydantic_compat import PrivateAttr
from evidently._pydantic_compat import parse_obj_as
from evidently.errors import EvidentlyError
from evidently.pydantic_utils import AutoAliasMixin
from evidently.pydantic_utils import EvidentlyBaseModel
from evidently.ui.service.type_aliases import STR_UUID
from evidently.ui.service.type_aliases import ZERO_UUID
from evidently.ui.service.type_aliases import ProjectID
from evidently.ui.service.type_aliases import UserID

if TYPE_CHECKING:
    from evidently.ui.workspace import RemoteWorkspace

ArtifactID = uuid.UUID
ArtifactVersionID = uuid.UUID

# Type aliases for user-facing APIs that accept both str and UUID
ArtifactIDInput = STR_UUID
ArtifactVersionIDInput = STR_UUID


class ArtifactContentType(str, Enum):
    """Type of content stored in an artifact.

    Determines how the artifact content is interpreted and used.
    """

    Prompt = "prompt"
    """Prompt template content."""
    Config = "config"
    """Configuration content."""
    Descriptor = "descriptor"
    """Descriptor definition content."""
    RunDescriptorsConfig = "run-descriptors-config"
    """Run descriptors configuration content."""


TArtifactValue = TypeVar("TArtifactValue")


class ArtifactContent(AutoAliasMixin, EvidentlyBaseModel, Generic[TArtifactValue], ABC):
    """Base class for artifact content wrappers.

    Artifact content wraps typed values (e.g., prompts, configs) for storage
    and versioning in the artifact system.
    """

    __alias_type__: ClassVar = "artifact_content"
    __value_class__: ClassVar[Type[TArtifactValue]]
    __value_type__: ClassVar[ArtifactContentType]

    class Config:
        is_base_type = True

    data: Any
    """Raw data stored in the artifact."""

    def get_value(self) -> TArtifactValue:
        """Extract the typed value from the content.

        Returns:
        * Typed value parsed from the stored data.
        """
        return parse_obj_as(self.__value_class__, self.data)

    def get_type(self) -> ArtifactContentType:
        """Get the content type.

        Returns:
        * `ArtifactContentType` indicating what kind of content this is.
        """
        return self.__value_type__

    @classmethod
    @abstractmethod
    def from_value(cls, value: TArtifactValue) -> "ArtifactContent":
        """Create content wrapper from a typed value.

        Args:
        * `value`: Typed value to wrap.

        Returns:
        * `ArtifactContent` instance wrapping the value.
        """
        raise NotImplementedError()

    def __init_subclass__(cls):
        _CONTENT_TYPE_MAPPING[cls.__value_class__] = cls
        super().__init_subclass__()


_CONTENT_TYPE_MAPPING: Dict[Type, Type[ArtifactContent]] = {}


def _parse_any_to_content(value: Any) -> ArtifactContent:
    for base_type, content_type in _CONTENT_TYPE_MAPPING.items():
        if isinstance(value, base_type):
            return content_type.from_value(value)
    raise ValueError(f"Cannot convert {value} to ArtifactContent")


class ArtifactMetadata(BaseModel):
    """Metadata for an artifact.

    Stores creation/update timestamps, author information, and optional description.
    """

    created_at: datetime = Field(default_factory=datetime.now)
    """Creation timestamp."""
    updated_at: datetime = Field(default_factory=datetime.now)
    """Last update timestamp."""
    author: Optional[UserID] = None
    """Optional user ID of the creator."""
    description: Optional[str] = None
    """Optional description of the artifact."""


class Artifact(BaseModel):
    """An artifact in the Evidently system.

    Artifacts are versioned objects that can store prompts, configs, descriptors,
    or other structured data. Each artifact has a name, metadata, and multiple versions.
    """

    id: ArtifactID = ZERO_UUID
    """Unique artifact identifier."""
    project_id: ProjectID = ZERO_UUID
    """Project this artifact belongs to."""
    name: str
    """Name of the artifact."""
    metadata: ArtifactMetadata = Field(default_factory=ArtifactMetadata)
    """Metadata about the artifact."""


class ArtifactVersionMetadata(BaseModel):
    """Metadata for an artifact version.

    Stores creation/update timestamps, author information, and optional comment
    describing the changes in this version.
    """

    created_at: datetime = Field(default_factory=datetime.now)
    """Creation timestamp."""
    updated_at: datetime = Field(default_factory=datetime.now)
    """Last update timestamp."""
    author: Optional[UserID] = None
    """Optional user ID of the creator."""
    comment: Optional[str] = None
    """Optional comment describing this version."""


class ArtifactVersion(BaseModel):
    """A version of an artifact.

    Each artifact can have multiple versions, allowing you to track changes
    over time and roll back if needed. Versions are numbered sequentially starting from 1.
    """

    id: ArtifactVersionID = ZERO_UUID
    """Unique version identifier."""
    artifact_id: ArtifactID = ZERO_UUID
    """ID of the parent artifact."""
    version: int
    """Version number (1, 2, 3, ...)."""
    metadata: ArtifactVersionMetadata = Field(default_factory=ArtifactVersionMetadata)
    """Metadata about this version."""
    content: ArtifactContent
    """The artifact content for this version."""
    content_type: ArtifactContentType
    """Type of content stored."""

    def __init__(
        self,
        content: Union[Any, ArtifactContent],
        version: int,
        id: ArtifactVersionID = ZERO_UUID,
        artifact_id: ArtifactID = ZERO_UUID,
        metadata: Optional[ArtifactVersionMetadata] = None,
        content_type: Optional[ArtifactContentType] = None,
        **data: Any,
    ):
        if not isinstance(content, ArtifactContent):
            try:
                content = parse_obj_as(ArtifactContent, content)  # type: ignore[type-abstract]
            except ValueError:
                content = _parse_any_to_content(content)

        if content_type is None:
            content_type = content.get_type()
        elif content_type != content.get_type():
            raise ValueError(f"Wrong content type for content {content.__class__.__name__}")

        super().__init__(
            content=content,
            version=version,
            id=id,
            artifact_id=artifact_id,
            metadata=metadata or ArtifactVersionMetadata(),
            content_type=content_type,
            **data,
        )


VersionOrLatest = Union[int, Literal["latest"]]
T = TypeVar("T")


class RemoteArtifact(Artifact):
    """Remote artifact with API access.

    Provides methods to interact with a remote artifact through the API,
    including version management and updates. Use `ArtifactAPI` to create
    and manage remote artifacts.
    """

    _api: "ArtifactAPI" = PrivateAttr()

    id: ArtifactID = ZERO_UUID
    """Unique artifact identifier."""
    project_id: ProjectID = ZERO_UUID
    """Project this artifact belongs to."""
    name: str
    """Name of the artifact."""
    metadata: ArtifactMetadata = Field(default_factory=ArtifactMetadata)
    """Metadata about the artifact."""

    def bind(self, api: "ArtifactAPI") -> "RemoteArtifact":
        """Bind this artifact to an API instance.

        Args:
        * `api`: `ArtifactAPI` to use for operations.

        Returns:
        * Self for method chaining.
        """
        self._api = api
        return self

    def list_versions(self) -> List[ArtifactVersion]:
        """List all versions of this artifact.

        Returns:
        * List of `ArtifactVersion` objects.
        """
        return self._api.list_versions(self.id)

    def get_version(self, version: VersionOrLatest = "latest") -> ArtifactVersion:
        """Get a specific version of this artifact.

        Args:
        * `version`: Version number or `"latest"`.

        Returns:
        * `ArtifactVersion` for the specified version.
        """
        return self._api.get_version(self.id, version)

    def bump_version(self, content: Any):
        """Create a new version with the given content.

        Args:
        * `content`: Content to store in the new version.

        Returns:
        * New `ArtifactVersion` with incremented version number.
        """
        return self._api.bump_artifact_version(self.id, content)

    def delete(self):
        """Delete this artifact and all its versions.

        This operation is irreversible and will permanently remove the artifact
        and all associated versions from the workspace.
        """
        return self._api.delete_artifact(self.id)

    def delete_version(self, version_id: ArtifactVersionID):
        """Delete a specific version.

        This operation is irreversible and will permanently remove the version.

        Args:
        * `version_id`: ID of the version to delete.
        """
        return self._api.delete_version(version_id)

    def save(self):
        """Save changes to this artifact's metadata to the remote workspace.

        Updates the artifact's name and metadata fields. Does not affect versions.
        """
        self._api.update_artifact(self)


class ArtifactAPI(ABC):
    """Abstract base class for artifact API."""

    @abstractmethod
    def list_artifacts(self, project_id: STR_UUID) -> List[RemoteArtifact]:
        """List all artifacts in a project."""
        ...

    @abstractmethod
    def get_or_create_artifact(self, project_id: STR_UUID, name: str) -> RemoteArtifact:
        """Get or create an artifact by name."""
        ...

    @abstractmethod
    def get_artifact(self, project_id: STR_UUID, name: str) -> RemoteArtifact:
        """Get an artifact by name."""
        ...

    @abstractmethod
    def get_artifact_by_id(self, project_id: STR_UUID, artifact_id: ArtifactIDInput) -> RemoteArtifact:
        """Get an artifact by ID."""
        ...

    @abstractmethod
    def create_artifact(self, project_id: STR_UUID, name: str) -> RemoteArtifact:
        """Create a new artifact."""
        ...

    @abstractmethod
    def delete_artifact(self, artifact_id: ArtifactIDInput):
        """Delete an artifact."""
        ...

    @abstractmethod
    def update_artifact(self, artifact: Artifact):
        """Update an artifact."""
        ...

    @abstractmethod
    def list_versions(self, artifact_id: ArtifactIDInput) -> List[ArtifactVersion]:
        """List all versions of an artifact."""
        ...

    @abstractmethod
    def get_version(self, artifact_id: ArtifactIDInput, version: VersionOrLatest = "latest") -> ArtifactVersion:
        """Get a specific version of an artifact."""
        ...

    @abstractmethod
    def get_version_by_id(self, artifact_version_id: ArtifactVersionIDInput) -> ArtifactVersion:
        """Get a version by its ID."""
        ...

    @abstractmethod
    def create_version(self, artifact_id: ArtifactIDInput, version: int, content: Any) -> ArtifactVersion:
        """Create a new version of an artifact."""
        ...

    @abstractmethod
    def delete_version(self, artifact_version_id: ArtifactVersionIDInput):
        """Delete a version."""
        ...

    @abstractmethod
    def bump_artifact_version(self, artifact_id: ArtifactIDInput, content: Any) -> ArtifactVersion:
        """Bump artifact version (create next version)."""
        ...


class RemoteArtifactAPI(ArtifactAPI):
    """Remote artifact API that works with /api/artifacts endpoint (OSS)."""

    def __init__(self, workspace: "RemoteWorkspace"):
        self._ws = workspace
        self._api_prefix = "/api/artifacts"

    def list_artifacts(self, project_id: STR_UUID) -> List[RemoteArtifact]:
        return [
            p.bind(self)
            for p in self._ws._request(
                f"{self._api_prefix}",
                "GET",
                query_params={"project_id": str(project_id)},
                response_model=List[RemoteArtifact],
            )
        ]

    def get_or_create_artifact(self, project_id: STR_UUID, name: str) -> RemoteArtifact:
        try:
            return self.get_artifact(project_id, name)
        except EvidentlyError as e:
            error_msg = e.get_message()
            if "artifact not found" not in error_msg.lower() and "Artifact not found" not in error_msg:
                raise e
            return self.create_artifact(project_id, name)

    def get_artifact(self, project_id: STR_UUID, name: str) -> RemoteArtifact:
        return self._ws._request(
            f"{self._api_prefix}/by-name/{name}",
            "GET",
            query_params={"project_id": str(project_id)},
            response_model=RemoteArtifact,
        ).bind(self)

    def get_artifact_by_id(self, project_id: STR_UUID, artifact_id: ArtifactIDInput) -> RemoteArtifact:
        return self._ws._request(f"{self._api_prefix}/{artifact_id}", "GET", response_model=RemoteArtifact).bind(self)

    def create_artifact(self, project_id: STR_UUID, name: str) -> RemoteArtifact:
        return self._ws._request(
            f"{self._api_prefix}/",
            "POST",
            query_params={"project_id": str(project_id)},
            body=Artifact(name=name, metadata=ArtifactMetadata()).dict(),
            response_model=RemoteArtifact,
        ).bind(self)

    def delete_artifact(self, artifact_id: ArtifactIDInput):
        return self._ws._request(f"{self._api_prefix}/{artifact_id}", "DELETE")

    def update_artifact(self, artifact: Artifact):
        self._ws._request(
            f"{self._api_prefix}/{artifact.id}",
            "PUT",
            body=json.loads(artifact.json()),
        )

    def list_versions(self, artifact_id: ArtifactIDInput) -> List[ArtifactVersion]:
        return self._ws._request(
            f"{self._api_prefix}/{artifact_id}/versions", "GET", response_model=List[ArtifactVersion]
        )

    def get_version(self, artifact_id: ArtifactIDInput, version: VersionOrLatest = "latest") -> ArtifactVersion:
        return self._ws._request(
            f"{self._api_prefix}/{artifact_id}/versions/{version}", "GET", response_model=ArtifactVersion
        )

    def get_version_by_id(self, artifact_version_id: ArtifactVersionIDInput) -> ArtifactVersion:
        return self._ws._request(
            f"{self._api_prefix}/artifact-versions/{artifact_version_id}", "GET", response_model=ArtifactVersion
        )

    def create_version(self, artifact_id: ArtifactIDInput, version: int, content: Any) -> ArtifactVersion:
        return self._ws._request(
            f"{self._api_prefix}/{artifact_id}/versions",
            "POST",
            body=ArtifactVersion(version=version, content=content).dict(),
            response_model=ArtifactVersion,
        )

    def delete_version(self, artifact_version_id: ArtifactVersionIDInput):
        self._ws._request(f"{self._api_prefix}/artifact-versions/{artifact_version_id}", "DELETE")

    def bump_artifact_version(self, artifact_id: ArtifactIDInput, content: Any) -> ArtifactVersion:
        try:
            latest = self.get_version(artifact_id)
            version = latest.version + 1
        except EvidentlyError as e:
            if e.get_message() != "EvidentlyError: Artifact version not found":
                raise e
            version = 1
        return self.create_version(artifact_id, version, content)
