import uuid
from abc import abstractmethod
from datetime import datetime
from enum import Enum
from typing import Any
from typing import ClassVar
from typing import Dict
from typing import List
from typing import Optional

from evidently._pydantic_compat import BaseModel
from evidently._pydantic_compat import Field
from evidently.legacy.utils.llm.prompts import PromptTemplate
from evidently.pydantic_utils import AutoAliasMixin
from evidently.pydantic_utils import EvidentlyBaseModel
from evidently.ui.service.type_aliases import ZERO_UUID
from evidently.ui.service.type_aliases import ProjectID
from evidently.ui.service.type_aliases import UserID

PromptID = uuid.UUID
PromptVersionID = uuid.UUID

OutputSchema = Dict[str, Any]


class PromptContentType(Enum):
    CHAT = "chat"
    TEMPLATE = "template"
    STRING = "string"


class PromptContent(AutoAliasMixin, EvidentlyBaseModel):
    __alias_type__: ClassVar = "prompt_content"

    class Config:
        is_base_type = True

    @abstractmethod
    def as_string(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def as_template(self) -> PromptTemplate:
        raise NotImplementedError

    @abstractmethod
    def list_placeholders(self) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def output_schema(self) -> Optional[OutputSchema]:
        raise NotImplementedError


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
