import json
import uuid
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
from evidently._pydantic_compat import parse_obj_as
from evidently.errors import EvidentlyError
from evidently.llm.prompts.content import PromptContent
from evidently.llm.prompts.content import PromptContentType
from evidently.llm.prompts.content import TextPromptContent
from evidently.ui.service.type_aliases import ZERO_UUID
from evidently.ui.service.type_aliases import ProjectID
from evidently.ui.service.type_aliases import UserID

if TYPE_CHECKING:
    from evidently.ui.workspace import CloudWorkspace

PromptID = uuid.UUID
PromptVersionID = uuid.UUID


class PromptMetadata(BaseModel):
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    author: Optional[UserID] = None


class Prompt(BaseModel):
    id: PromptID = ZERO_UUID
    project_id: ProjectID = ZERO_UUID
    name: str
    metadata: PromptMetadata = PromptMetadata()


class PromptVersionMetadata(BaseModel):
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    author: Optional[UserID] = None


class PromptVersion(BaseModel):
    id: PromptVersionID = ZERO_UUID
    prompt_id: PromptID = ZERO_UUID
    version: int
    metadata: PromptVersionMetadata = PromptVersionMetadata()
    content: PromptContent
    content_type: PromptContentType

    def __init__(
        self,
        content: Union[str, PromptContent],
        version: int,
        id: PromptVersionID = ZERO_UUID,
        prompt_id: PromptID = ZERO_UUID,
        metadata: Optional[PromptVersionMetadata] = None,
        content_type: Optional[PromptContentType] = None,
        **data: Any,
    ):
        content = TextPromptContent(text=content) if isinstance(content, str) else content
        if not isinstance(content, PromptContent):
            content = parse_obj_as(PromptContent, content)
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
    _manager: "RemotePromptManager" = PrivateAttr()

    def bind(self, manager: "RemotePromptManager") -> "RemotePrompt":
        self._manager = manager
        return self

    def list_versions(self) -> List[PromptVersion]:
        return self._manager.list_versions(self.id)

    def get_version(self, version: VersionOrLatest = "latest") -> PromptVersion:
        return self._manager.get_version(self.id, version)

    def bump_version(self, content: str):
        return self._manager.bump_prompt_version(self.id, content)

    def delete(self):
        return self._manager.delete_prompt(self.id)

    def delete_version(self, version_id: PromptVersionID):
        return self._manager.delete_version(version_id)

    def save(self):
        self._manager.update_prompt(self)


class RemotePromptManager:
    def __init__(self, workspace: "CloudWorkspace"):
        self._ws = workspace

    def list_prompts(self, project_id: ProjectID) -> List[RemotePrompt]:
        return [
            p.bind(self)
            for p in self._ws._request(
                "/api/prompts", "GET", query_params={"project_id": project_id}, response_model=List[RemotePrompt]
            )
        ]

    def get_or_create_prompt(self, project_id: ProjectID, name: str) -> RemotePrompt:
        try:
            return self.get_prompt(project_id, name)
        except EvidentlyError as e:
            if not e.get_message() == "EvidentlyError: prompt not found":
                raise e
            return self.create_prompt(project_id, name)

    def get_prompt(self, project_id: ProjectID, name: str) -> RemotePrompt:
        return self._ws._request(
            f"/api/prompts/by-name/{name}", "GET", query_params={"project_id": project_id}, response_model=RemotePrompt
        ).bind(self)

    def get_prompt_by_id(self, project_id: ProjectID, prompt_id: PromptID) -> RemotePrompt:
        return self._ws._request(f"/api/prompts/{prompt_id}", "GET", response_model=RemotePrompt).bind(self)

    def create_prompt(self, project_id: ProjectID, name: str) -> RemotePrompt:
        return self._ws._request(
            "/api/prompts/",
            "POST",
            query_params={"project_id": project_id},
            body=Prompt(name=name, metadata=PromptMetadata()).dict(),
            response_model=RemotePrompt,
        ).bind(self)

    def delete_prompt(self, prompt_id: PromptID):
        return self._ws._request(f"/api/prompts/{prompt_id}", "DELETE")

    def update_prompt(self, prompt: Prompt):
        self._ws._request(
            f"/api/prompts/{prompt.id}",
            "PUT",
            body=json.loads(prompt.json()),
        )

    def list_versions(self, prompt_id: PromptID) -> List[PromptVersion]:
        return self._ws._request(f"/api/prompts/{prompt_id}/versions", "GET", response_model=List[PromptVersion])

    def get_version(self, prompt_id: PromptID, version: VersionOrLatest = "latest") -> PromptVersion:
        return self._ws._request(f"/api/prompts/{prompt_id}/versions/{version}", "GET", response_model=PromptVersion)

    def get_version_by_id(self, prompt_version_id: PromptVersionID) -> PromptVersion:
        return self._ws._request(
            f"/api/prompts/prompt-versions/{prompt_version_id}", "GET", response_model=PromptVersion
        )

    def create_version(self, prompt_id: PromptID, version: int, content: str) -> PromptVersion:
        return self._ws._request(
            f"/api/prompts/{prompt_id}/versions",
            "POST",
            body=PromptVersion(version=version, content=content).dict(),
            response_model=PromptVersion,
        )

    def delete_version(self, prompt_version_id: PromptVersionID):
        self._ws._request(f"/api/prompts/prompt-versions/{prompt_version_id}", "DELETE")

    def bump_prompt_version(self, prompt_id: PromptID, content: str) -> PromptVersion:
        # todo: single request?
        try:
            latest = self.get_version(prompt_id)
            version = latest.version + 1
        except EvidentlyError as e:
            if e.get_message() != "EvidentlyError: prompt version not found":
                raise e
            version = 1
        return self.create_version(prompt_id, version, content)
