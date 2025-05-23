from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple

from evidently import ColumnType
from evidently._pydantic_compat import PrivateAttr
from evidently.legacy.features.llm_judge import BaseLLMPromptTemplate
from evidently.legacy.utils.llm.prompts import JsonOutputFormatBlock
from evidently.legacy.utils.llm.prompts import OutputFormatBlock
from evidently.legacy.utils.llm.prompts import PromptBlock as PromptBlockV1
from evidently.legacy.utils.llm.prompts import PromptTemplate
from evidently.llm.prompts.blocks import Placeholder
from evidently.llm.prompts.blocks import PromptBlock
from evidently.llm.prompts.models import OutputSchema
from evidently.llm.prompts.models import PromptContent
from evidently.llm.prompts.schema import JsonLLMResponseSchema
from evidently.llm.prompts.schema import LLMResponseSchema
from evidently.llm.prompts.schema import PlainLLMResponseSchema


def get_response_schema(blocks: List[PromptBlock]) -> LLMResponseSchema:
    try:
        return next(b.get_response_schema() for b in blocks if b.get_response_schema() is not None)
    except StopIteration:
        return PlainLLMResponseSchema()


class GenericLLMPromptTemplate(BaseLLMPromptTemplate):
    class Config:
        type_alias = "evidently:prompt_template:GenericLLMPromptTemplate"

    blocks: List[PromptBlock]
    _response_schema: LLMResponseSchema = PrivateAttr()

    @property
    def response_schema(self) -> LLMResponseSchema:
        try:
            return self._response_schema
        except AttributeError:
            self._response_schema = get_response_schema(self.blocks)
        return self._response_schema

    def list_output_columns(self) -> List[str]:
        raise NotImplementedError()

    def get_type(self, subcolumn: Optional[str]) -> ColumnType:
        raise NotImplementedError()

    def get_main_output_column(self) -> str:
        raise NotImplementedError()

    def get_blocks(self) -> Sequence[PromptBlockV1]:
        return self.blocks

    def get_output_format(self) -> OutputFormatBlock:
        rs = self.response_schema
        if isinstance(rs, JsonLLMResponseSchema):
            return JsonOutputFormatBlock(fields={})
        raise NotImplementedError()


class TemplatePromptContent(PromptContent):
    blocks: List[PromptBlock]

    def as_string(self) -> str:
        return "\n".join(b.render() for b in self.blocks)

    def as_template(self) -> PromptTemplate:
        return GenericLLMPromptTemplate(blocks=self.blocks)

    def list_placeholders(self) -> List[Placeholder]:
        return [p for b in self.blocks for p in b.list_placeholders()]

    def output_schema(self) -> Optional[OutputSchema]:
        raise NotImplementedError


class ChatPromptContent(PromptContent):
    messages: List[Tuple[str, TemplatePromptContent]]

    def as_string(self) -> str:
        return "\n\n".join(f"{role}: {t.as_string()}" for role, t in self.messages)

    def as_template(self) -> PromptTemplate:
        raise NotImplementedError

    def list_placeholders(self) -> List[Placeholder]:
        return [p for _, t in self.messages for p in t.list_placeholders()]

    def output_schema(self) -> Optional[OutputSchema]:
        if len(self.messages) == 0:
            return None
        return self.messages[-1][1].output_schema()
