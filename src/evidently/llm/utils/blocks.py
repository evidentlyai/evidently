import inspect
import json
import re
from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import ClassVar
from typing import Dict
from typing import Generic
from typing import List
from typing import Tuple
from typing import TypeVar
from typing import Union

from evidently.llm.utils.errors import LLMResponseParseError
from evidently.llm.utils.parsing import get_tags
from evidently.pydantic_utils import AutoAliasMixin
from evidently.pydantic_utils import EvidentlyBaseModel


class PromptBlock(AutoAliasMixin, EvidentlyBaseModel):
    __alias_type__: ClassVar[str] = "prompt_block"

    class Config:
        is_base_type = True
        extra = "forbid"

    def _get_class_doc(self):
        doc = inspect.getdoc(self.__class__)
        if doc is None:
            raise ValueError("No docstring for this block")
        return doc

    def render(self) -> str:
        result = self._get_class_doc()
        for field in self.__fields__:
            placeholder = f"{{{field}}}"
            if placeholder in result:
                val = getattr(self, field)
                if isinstance(val, PromptBlock):
                    val = val.render()
                result = result.replace(placeholder, val if val is not None else "")
        return result

    def __str__(self):
        return self.render()

    @classmethod
    def simple(cls, value: str):
        return SimpleBlock(value=value)

    @classmethod
    def input(cls, placeholder_name: str = "input"):
        return SimpleBlock(value=f"{{{placeholder_name}}}")

    @classmethod
    def json_output(cls, **fields: Union[str, Tuple[str, str]]):
        return JsonOutputFormatBlock(fields=fields)

    @classmethod
    def string_list_output(cls, of_what: str, tagged: bool = False):
        if tagged:
            return TagStringListFormatBlock(of_what=of_what)
        return StringListFormatBlock(of_what=of_what)

    @classmethod
    def string_output(cls, what: str):
        return StringFormatBlock(what=what)

    def anchored(self, start: str = "__start__", end: str = "__end__"):
        return Anchor(start=start, block=self, end=end)

    def tag(self, tag_name: str):
        return Tag(tag_name=tag_name, block=self)


class Anchor(PromptBlock):
    """{start}\n{block}\n{end}"""

    start: str
    block: PromptBlock
    end: str


class Tag(PromptBlock):
    """<{tag_name}>\n{block}\n</{tag_name}>"""

    tag_name: str
    block: PromptBlock


class SimpleBlock(PromptBlock):
    """{value}"""

    value: str


class CompositePromptBlock(PromptBlock):
    def render(self) -> str:
        return "\n".join(b.render() for b in self.get_sub_blocks())

    def get_sub_blocks(self) -> List[PromptBlock]:
        res = []
        for field in self.__fields__.values():
            ft = field.type_
            if isinstance(ft, type) and issubclass(ft, PromptBlock):
                fv = getattr(self, field.name)
                if isinstance(fv, PromptBlock):
                    res.append(fv)
        return res


TResult = TypeVar("TResult")


class OutputFormatBlock(PromptBlock, ABC, Generic[TResult]):
    @abstractmethod
    def parse_response(self, response: str) -> TResult:
        raise NotImplementedError


class NoopOutputFormat(OutputFormatBlock[str]):
    def render(self) -> str:
        return ""

    def parse_response(self, response: str) -> str:
        return response


_json_pattern = re.compile(r"\{(?:[^{}]|\{[^{}]*\})*\}")


def find_largest_json(text):
    candidates = _json_pattern.findall(text)

    largest_json = None
    max_length = 0
    for candidate in candidates:
        try:
            json_obj = json.loads(candidate)
            if len(candidate) > max_length:
                largest_json = json_obj
                max_length = len(candidate)
        except json.JSONDecodeError:
            continue
    return largest_json


class JsonOutputFormatBlock(OutputFormatBlock[Dict[str, Any]]):
    fields: Dict[str, Union[Tuple[str, str], str]]
    search_for_substring: bool = True

    def render(self) -> str:
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

    def parse_response(self, response: str) -> Dict[str, Any]:
        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            if self.search_for_substring:
                sub = find_largest_json(response)
                if sub is not None:
                    return sub
            raise LLMResponseParseError("Failed to parse response as json", response) from e


class StringListFormatBlock(OutputFormatBlock[List[str]]):
    """Return a list of {of_what}.
    This should be only a list of string {of_what}, each one on a new line with no enumeration"""

    of_what: str

    def parse_response(self, response: str) -> List[str]:
        return [line.strip() for line in response.split("\n") if line.strip()]


class TagStringListFormatBlock(OutputFormatBlock[List[str]]):
    """Return a list of {of_what}.
    This should be only a list of string {of_what}, each one inside <{of_what}></{of_what}> tag"""

    of_what: str

    def parse_response(self, response: str) -> List[str]:
        return get_tags(response, self.of_what)


class StringFormatBlock(OutputFormatBlock[str]):
    """Return {what} only."""

    what: str

    def parse_response(self, response: str) -> str:
        return response
