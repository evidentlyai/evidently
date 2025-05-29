import re
from abc import abstractmethod
from typing import Any
from typing import ClassVar
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

from evidently.llm.prompts.schema import JsonLLMResponseSchema
from evidently.llm.prompts.schema import LLMResponseSchema
from evidently.llm.prompts.utils import partial_format
from evidently.pydantic_utils import AutoAliasMixin
from evidently.pydantic_utils import EvidentlyBaseModel

Placeholder = str  # potentially tuple[name, type]


class PromptBlock(AutoAliasMixin, EvidentlyBaseModel):
    __alias_type__: ClassVar[str] = "prompt_block_2"

    class Config:
        is_base_type = True

    @abstractmethod
    def list_placeholders(self) -> List[Placeholder]:
        raise NotImplementedError

    @abstractmethod
    def render(self, values: Optional[Dict[str, Any]] = None) -> str:
        raise NotImplementedError

    def get_response_schema(self) -> Optional[LLMResponseSchema]:
        return None

    @classmethod
    def simple(cls, content: str) -> "PromptBlock":
        return SimplePromptBlock(content=content)


placeholders_re = re.compile(r"\{([a-zA-Z0-9_]+)}")


class SimplePromptBlock(PromptBlock):
    content: str

    def list_placeholders(self) -> List[Placeholder]:
        return list(placeholders_re.findall(self.content))

    def render(self, values: Optional[Dict[str, Any]] = None) -> str:
        if values is None:
            return self.content
        return partial_format(self.content, values)


class JsonOutputBlock(PromptBlock):
    fields: Dict[str, Union[Tuple[str, str], str]]
    search_for_substring: bool = True

    def _render(self) -> str:
        values = []
        example_rows = []
        for field, descr in self.fields.items():
            if isinstance(descr, tuple):
                descr, field_key = descr
            else:
                field_key = field
            values.append(field)
            example_rows.append(f'"{field_key}": "{descr}"')

        example_rows_str = "\n".join(example_rows)
        return f"Return {', '.join(values)} formatted as json without formatting as follows:\n{{{{\n{example_rows_str}\n}}}}"

    def list_placeholders(self) -> List[Placeholder]:
        return list(placeholders_re.findall(self._render()))

    def render(self, values: Optional[Dict[str, Any]] = None) -> str:
        return partial_format(self._render(), values)

    def get_response_schema(self) -> Optional[LLMResponseSchema]:
        # dunno
        return JsonLLMResponseSchema(json_schema={f: {"type": "string"} for f in self.fields})


# class ClassificationPromptBlock(PromptBlock):
#     where: str = ""
#     what: str = "text"
#     into_what: str = "categories"
#     categories: List[str]
#
#     def render(self, values: Optional[Dict[str, Any]] = None) -> str:
#         if len(self.categories) < 2:
#             raise ValueError("should be at least 2 categories")
#         cats = ", ".join(self.categories[:-1]) + " and " + self.categories[-1]
#         cont =  f"Classify {self.what} {self.where} "\
#                 f"into {len(self.categories)} {self.into_what}: {cats}."
#         return cont
#
#     def list_placeholders(self) -> List[Placeholder]:
#         return []
