import json
import uuid
from abc import ABC
from abc import abstractmethod
from datetime import datetime
from typing import TYPE_CHECKING
from typing import Any
from typing import List
from typing import Literal
from typing import Optional
from typing import Union

from evidently._pydantic_compat import BaseModel
from evidently._pydantic_compat import Field
from evidently._pydantic_compat import PrivateAttr
from evidently._pydantic_compat import ValidationError
from evidently._pydantic_compat import parse_obj_as
from evidently.errors import EvidentlyError
from evidently.llm.prompts.content import PromptContent
from evidently.llm.prompts.content import PromptContentType
from evidently.ui.service.type_aliases import STR_UUID
from evidently.ui.service.type_aliases import ZERO_UUID
from evidently.ui.service.type_aliases import ProjectID
from evidently.ui.service.type_aliases import UserID

if TYPE_CHECKING:
    from evidently.ui.workspace import CloudWorkspace

PromptID = uuid.UUID
PromptVersionID = uuid.UUID

# Type aliases for user-facing APIs that accept both str and UUID
PromptIDInput = STR_UUID
PromptVersionIDInput = STR_UUID


class PromptMetadata(BaseModel):
    """Metadata for a prompt.

    Stores creation/update timestamps and author information.
    """

    created_at: datetime = Field(default_factory=datetime.now)
    """Creation timestamp."""
    updated_at: datetime = Field(default_factory=datetime.now)
    """Last update timestamp."""
    author: Optional[UserID] = None
    """Optional user ID of the creator."""


class Prompt(BaseModel):
    """A prompt in the Evidently system.

    Prompts are versioned objects that store prompt templates for LLM interactions.
    Each prompt can have multiple versions to track changes over time.
    """

    id: PromptID = ZERO_UUID
    """Unique prompt identifier."""
    project_id: ProjectID = ZERO_UUID
    """Project this prompt belongs to."""
    name: str
    """Name of the prompt."""
    metadata: PromptMetadata = Field(default_factory=PromptMetadata)
    """Metadata about the prompt."""


class PromptVersionMetadata(BaseModel):
    """Metadata for a prompt version.

    Stores creation/update timestamps and author information for a specific version.
    """

    created_at: datetime = Field(default_factory=datetime.now)
    """Creation timestamp."""
    updated_at: datetime = Field(default_factory=datetime.now)
    """Last update timestamp."""
    author: Optional[UserID] = None
    """Optional user ID of the creator."""


class PromptVersion(BaseModel):
    """A version of a prompt.

    Each prompt can have multiple versions, allowing you to track changes
    over time and roll back if needed. Versions are numbered sequentially starting from 1.
    """

    id: PromptVersionID = ZERO_UUID
    """Unique version identifier."""
    prompt_id: PromptID = ZERO_UUID
    """ID of the parent prompt."""
    version: int
    """Version number (1, 2, 3, ...)."""
    metadata: PromptVersionMetadata = Field(default_factory=PromptVersionMetadata)
    """Metadata about this version."""
    content: PromptContent
    """The prompt content for this version."""
    content_type: PromptContentType
    """Type of prompt content."""

    def __init__(
        self,
        content: Union[Any, PromptContent],
        version: int,
        id: PromptVersionID = ZERO_UUID,
        prompt_id: PromptID = ZERO_UUID,
        metadata: Optional[PromptVersionMetadata] = None,
        content_type: Optional[PromptContentType] = None,
        **data: Any,
    ):
        if not isinstance(content, PromptContent):
            try:
                content = parse_obj_as(PromptContent, content)  # type: ignore[type-abstract]
            except ValidationError:
                content = PromptContent.parse(content)
        if content_type is None:
            content_type = content.get_type()
        elif content_type != content.get_type():
            raise ValueError(f"Wrong content type for content {content.__class__.__name__}")

        super().__init__(
            content=content,
            version=version,
            id=id,
            prompt_id=prompt_id,
            metadata=metadata or PromptVersionMetadata(),
            content_type=content_type,
            **data,
        )


VersionOrLatest = Union[int, Literal["latest"]]


class RemotePrompt(Prompt):
    """Remote prompt with API access.

    Provides methods to interact with a remote prompt through the API,
    including version management and updates. Use `PromptAPI` to create
    and manage remote prompts.
    """

    _api: "PromptAPI" = PrivateAttr()

    id: PromptID = ZERO_UUID
    """Unique prompt identifier."""
    project_id: ProjectID = ZERO_UUID
    """Project this prompt belongs to."""
    name: str
    """Name of the prompt."""
    metadata: PromptMetadata = Field(default_factory=PromptMetadata)
    """Metadata about the prompt."""

    def bind(self, api: "PromptAPI") -> "RemotePrompt":
        """Bind this prompt to an API instance.

        Args:
        * `api`: `PromptAPI` to use for operations.

        Returns:
        * Self for method chaining.
        """
        self._api = api
        return self

    def list_versions(self) -> List[PromptVersion]:
        """List all versions of this prompt.

        Returns:
        * List of `PromptVersion` objects.
        """
        return self._api.list_versions(self.id)

    def get_version(self, version: VersionOrLatest = "latest") -> PromptVersion:
        """Get a specific version of this prompt.

        Args:
        * `version`: Version number or `"latest"`.

        Returns:
        * `PromptVersion` for the specified version.
        """
        return self._api.get_version(self.id, version)

    def bump_version(self, content: Any):
        """Create a new version with the given content.

        Args:
        * `content`: Content to store in the new version.

        Returns:
        * New `PromptVersion` with incremented version number.
        """
        return self._api.bump_prompt_version(self.id, content)

    def delete(self):
        """Delete this prompt and all its versions.

        This operation is irreversible and will permanently remove the prompt
        and all associated versions from the workspace.
        """
        return self._api.delete_prompt(self.id)

    def delete_version(self, version_id: PromptVersionID):
        """Delete a specific version.

        This operation is irreversible and will permanently remove the version.

        Args:
        * `version_id`: ID of the version to delete.
        """
        return self._api.delete_version(version_id)

    def save(self):
        """Save changes to this prompt's metadata to the remote workspace.

        Updates the prompt's name and metadata fields. Does not affect versions.
        """
        self._api.update_prompt(self)


class PromptAPI(ABC):
    """Abstract base class for prompt API."""

    @abstractmethod
    def list_prompts(self, project_id: STR_UUID) -> List[RemotePrompt]:
        """List all prompts in a project."""
        ...

    @abstractmethod
    def get_or_create_prompt(self, project_id: STR_UUID, name: str) -> RemotePrompt:
        """Get or create a prompt by name."""
        ...

    @abstractmethod
    def get_prompt(self, project_id: STR_UUID, name: str) -> RemotePrompt:
        """Get a prompt by name."""
        ...

    @abstractmethod
    def get_prompt_by_id(self, project_id: STR_UUID, prompt_id: PromptIDInput) -> RemotePrompt:
        """Get a prompt by ID."""
        ...

    @abstractmethod
    def create_prompt(self, project_id: STR_UUID, name: str) -> RemotePrompt:
        """Create a new prompt."""
        ...

    @abstractmethod
    def delete_prompt(self, prompt_id: PromptIDInput):
        """Delete a prompt."""
        ...

    @abstractmethod
    def update_prompt(self, prompt: Prompt):
        """Update a prompt."""
        ...

    @abstractmethod
    def list_versions(self, prompt_id: PromptIDInput) -> List[PromptVersion]:
        """List all versions of a prompt."""
        ...

    @abstractmethod
    def get_version(self, prompt_id: PromptIDInput, version: VersionOrLatest = "latest") -> PromptVersion:
        """Get a specific version of a prompt."""
        ...

    @abstractmethod
    def get_version_by_id(self, prompt_version_id: PromptVersionIDInput) -> PromptVersion:
        """Get a version by its ID."""
        ...

    @abstractmethod
    def create_version(self, prompt_id: PromptIDInput, version: int, content: Any) -> PromptVersion:
        """Create a new version of a prompt."""
        ...

    @abstractmethod
    def delete_version(self, prompt_version_id: PromptVersionIDInput):
        """Delete a version."""
        ...

    @abstractmethod
    def bump_prompt_version(self, prompt_id: PromptIDInput, content: Any) -> PromptVersion:
        """Bump prompt version (create next version)."""
        ...


class CloudPromptAPI(PromptAPI):
    """Cloud-only prompt API that works with /api/prompts endpoint."""

    def __init__(self, workspace: "CloudWorkspace"):
        self._ws = workspace

    def list_prompts(self, project_id: STR_UUID) -> List[RemotePrompt]:
        return [
            p.bind(self)
            for p in self._ws._request(
                "/api/prompts", "GET", query_params={"project_id": str(project_id)}, response_model=List[RemotePrompt]
            )
        ]

    def get_or_create_prompt(self, project_id: STR_UUID, name: str) -> RemotePrompt:
        try:
            return self.get_prompt(project_id, name)
        except EvidentlyError as e:
            if not e.get_message() == "EvidentlyError: prompt not found":
                raise e
            return self.create_prompt(project_id, name)

    def get_prompt(self, project_id: STR_UUID, name: str) -> RemotePrompt:
        return self._ws._request(
            f"/api/prompts/by-name/{name}",
            "GET",
            query_params={"project_id": str(project_id)},
            response_model=RemotePrompt,
        ).bind(self)

    def get_prompt_by_id(self, project_id: STR_UUID, prompt_id: PromptIDInput) -> RemotePrompt:
        return self._ws._request(f"/api/prompts/{prompt_id}", "GET", response_model=RemotePrompt).bind(self)

    def create_prompt(self, project_id: STR_UUID, name: str) -> RemotePrompt:
        return self._ws._request(
            "/api/prompts/",
            "POST",
            query_params={"project_id": str(project_id)},
            body=Prompt(name=name, metadata=PromptMetadata()).dict(),
            response_model=RemotePrompt,
        ).bind(self)

    def delete_prompt(self, prompt_id: PromptIDInput):
        return self._ws._request(f"/api/prompts/{prompt_id}", "DELETE")

    def update_prompt(self, prompt: Prompt):
        self._ws._request(
            f"/api/prompts/{prompt.id}",
            "PUT",
            body=json.loads(prompt.json()),
        )

    def list_versions(self, prompt_id: PromptIDInput) -> List[PromptVersion]:
        return self._ws._request(f"/api/prompts/{prompt_id}/versions", "GET", response_model=List[PromptVersion])

    def get_version(self, prompt_id: PromptIDInput, version: VersionOrLatest = "latest") -> PromptVersion:
        return self._ws._request(f"/api/prompts/{prompt_id}/versions/{version}", "GET", response_model=PromptVersion)

    def get_version_by_id(self, prompt_version_id: PromptVersionIDInput) -> PromptVersion:
        return self._ws._request(
            f"/api/prompts/prompt-versions/{prompt_version_id}", "GET", response_model=PromptVersion
        )

    def create_version(self, prompt_id: PromptIDInput, version: int, content: Any) -> PromptVersion:
        return self._ws._request(
            f"/api/prompts/{prompt_id}/versions",
            "POST",
            body=PromptVersion(version=version, content=content).dict(),
            response_model=PromptVersion,
        )

    def delete_version(self, prompt_version_id: PromptVersionIDInput):
        self._ws._request(f"/api/prompts/prompt-versions/{prompt_version_id}", "DELETE")

    def bump_prompt_version(self, prompt_id: PromptIDInput, content: Any) -> PromptVersion:
        # todo: single request?
        try:
            latest = self.get_version(prompt_id)
            version = latest.version + 1
        except EvidentlyError as e:
            if e.get_message() != "EvidentlyError: prompt version not found":
                raise e
            version = 1
        return self.create_version(prompt_id, version, content)
