import uuid
from datetime import datetime
from typing import TYPE_CHECKING
from typing import Optional

from evidently._pydantic_compat import BaseModel
from evidently._pydantic_compat import Field
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
    metadata: PromptMetadata = PromptMetadata


class PromptVersionMetadata(BaseModel):
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    author: Optional[UserID] = None


class PromptVersion(BaseModel):
    id: PromptVersionID = ZERO_UUID
    prompt_id: PromptID = ZERO_UUID
    version: str
    metadata: PromptVersionMetadata = PromptVersionMetadata()
    content: str


class RemotePromptManager:
    def __init__(self, workspace: "CloudWorkspace"):
        self._ws = workspace

    def get_or_create_prompt(self, project_id: ProjectID, name: str) -> Prompt:
        prompt = self.get_prompt(project_id, name)
        if prompt is None:
            return self.create_prompt(project_id, name)
        return prompt

    def get_prompt(self, project_id: ProjectID, name: str) -> Prompt:
        return self._ws._request(
            f"/api/prompts/{project_id}/prompt-by-name", "GET", query_params={"name": name}, response_model=Prompt
        )

    def get_prompt_by_id(self, prompt_id: PromptID) -> Prompt:
        return self._ws._request("/api/prompts", "GET", response_model=Prompt)

    def create_prompt(self, project_id: ProjectID, name: str) -> Prompt:
        return self._ws._request(
            f"/api/prompts/{project_id}",
            "POST",
            body=Prompt(name=name, metadata=PromptMetadata()).dict(),
            response_model=Prompt,
        )

    def get_version(self, prompt_id: PromptID, version: str) -> PromptVersion:
        project_id = self.get_prompt_by_id(prompt_id).project_id
        return self._ws._request(
            f"/api/prompts/{project_id}/prompts/{prompt_id}/version/{version}", "GET", response_model=PromptVersion
        )

    def create_version(self, prompt_id: PromptID, version: str, content: str) -> PromptVersion:
        project_id = self.get_prompt_by_id(prompt_id).project_id
        return self._ws._request(
            f"/api/prompts/{project_id}/prompts/{prompt_id}/versions/",
            "POST",
            body=PromptVersion(version=version, content=content).dict(),
            response_model=PromptVersion,
        )
