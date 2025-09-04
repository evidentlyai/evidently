from abc import abstractmethod
from enum import Enum
from typing import ClassVar
from typing import List

from evidently.legacy.core import new_id
from evidently.llm.models import LLMMessage
from evidently.llm.templates import BaseLLMPromptTemplate
from evidently.pydantic_utils import AutoAliasMixin
from evidently.pydantic_utils import EvidentlyBaseModel


class PromptContentType(str, Enum):
    TEXT = "text"
    MESSAGES = "messages"
    JUDGE = "judge"
    TEMPLATE = "template"


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


class TemplatePromptContent(PromptContent):
    template: BaseLLMPromptTemplate

    def as_text(self) -> str:
        return "\n".join(f"{m.role}: {m.content}" for m in self.as_messages())

    def as_messages(self) -> List[LLMMessage]:
        template = self.template
        placeholder_map = {ph: str(new_id()) for ph in template.prepared_template.placeholders}
        result = []
        # replace actual placeholders with random uuid
        # this will also turn non-placeholders like {{ ... }} into placeholder
        for message in template.get_messages(values=placeholder_map):
            # turn fake placeholders back
            content = message.content.replace("{", "{{").replace("}", "}}")
            for ph, key in placeholder_map.items():
                content = content.replace(str(key), f"{{{ph}}}")
            result.append(LLMMessage(role=message.role, content=content))
        return result

    def get_type(self) -> PromptContentType:
        return PromptContentType.TEMPLATE
