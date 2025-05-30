from abc import abstractmethod
from enum import Enum
from typing import ClassVar
from typing import List

from evidently.llm.models import LLMMessage
from evidently.pydantic_utils import AutoAliasMixin
from evidently.pydantic_utils import EvidentlyBaseModel


class PromptContentType(str, Enum):
    TEXT = "text"
    MESSAGES = "messages"


class PromptContent(AutoAliasMixin, EvidentlyBaseModel):
    __alias_type__: ClassVar = "prompt_content"

    class Config:
        is_base_type = True

    @abstractmethod
    def as_text(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def as_messages(self) -> List[LLMMessage]:
        raise NotImplementedError

    def get_type(self) -> PromptContentType:
        return PromptContentType.TEXT


class TextPromptContent(PromptContent):
    text: str

    def as_text(self) -> str:
        return self.text

    def as_messages(self) -> List[LLMMessage]:
        return [LLMMessage.user(self.text)]


class MessagesPromptContent(PromptContent):
    messages: List[LLMMessage]

    def as_text(self) -> str:
        return "\n".join(f"{m.role}: {m.content}" for m in self.messages)

    def as_messages(self) -> List[LLMMessage]:
        return self.messages

    def get_type(self) -> PromptContentType:
        return PromptContentType.MESSAGES
