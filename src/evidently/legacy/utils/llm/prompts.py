import inspect
import json
import re
from abc import ABC
from abc import abstractmethod
from functools import wraps
from typing import Any
from typing import Callable
from typing import ClassVar
from typing import Dict
from typing import Generic
from typing import Iterator
from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Type
from typing import TypeVar
from typing import Union

import typing_inspect

from evidently.legacy.utils.llm.base import LLMMessage
from evidently.legacy.utils.llm.errors import LLMResponseParseError
from evidently.legacy.utils.llm.wrapper import LLMRequest
from evidently.pydantic_utils import EvidentlyBaseModel

TResult = TypeVar("TResult")


class PromptBlock(EvidentlyBaseModel):
    class Config:
        is_base_type = True

    def render(self):
        # )))
        result = self._render()
        for field in self.__fields__:
            placeholder = f"{{{field}}}"
            if placeholder in result:
                result = result.replace(placeholder, getattr(self, field))
        return result

    @abstractmethod
    def _render(self) -> str:
        raise NotImplementedError

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
    def string_list_output(cls, of_what: str):
        return StringListFormatBlock(of_what=of_what)

    @classmethod
    def string_output(cls, what: str):
        return StringFormatBlock(what=what)

    def anchored(self, start: str = "__start__", end: str = "__end__"):
        return Anchor(start=start, block=self, end=end)


class Anchor(PromptBlock):
    class Config:
        type_alias = "evidently:prompt_block:Anchor"

    start: str
    block: PromptBlock
    end: str

    def _render(self) -> str:
        return f"{self.start}\n{self.block.render()}\n{self.end}"


class SimpleBlock(PromptBlock):
    class Config:
        type_alias = "evidently:prompt_block:SimpleBlock"

    value: str

    def _render(self) -> str:
        return self.value


class OutputFormatBlock(PromptBlock, ABC, Generic[TResult]):
    @abstractmethod
    def parse_response(self, response: str) -> TResult:
        raise NotImplementedError


class NoopOutputFormat(OutputFormatBlock[str]):
    class Config:
        type_alias = "evidently:prompt_block:NoopOutputFormat"

    def _render(self) -> str:
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
    class Config:
        type_alias = "evidently:prompt_block:JsonOutputFormatBlock"

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
    class Config:
        type_alias = "evidently:prompt_block:StringListFormatBlock"

    of_what: str

    def _render(self) -> str:
        return f"""Return a list of {self.of_what}.
This should be only a list of string {self.of_what}, each one on a new line with no enumeration"""

    def parse_response(self, response: str) -> List[str]:
        return [line.strip() for line in response.split("\n") if line.strip()]


class StringFormatBlock(OutputFormatBlock[str]):
    class Config:
        type_alias = "evidently:prompt_block:StringFormatBlock"

    what: str

    def _render(self) -> str:
        return f"""Return {self.what} only."""

    def parse_response(self, response: str) -> str:
        return response


def llm_call(f: Callable) -> Callable[..., LLMRequest]:
    sig = inspect.getfullargspec(f)
    response_type = sig.annotations.get("return", str)

    @wraps(f)
    def inner(self: PromptTemplate, *args, **kwargs):
        kwargs = inspect.getcallargs(f, *args, **kwargs, self=self)
        del kwargs["self"]
        template = self.get_template()
        placeholders = self.list_placeholders(template)
        if set(placeholders) != set(kwargs.keys()):
            raise TypeError(
                f"{f} arg signature ({list(kwargs)}) does not correspond to placeholders in prompt ({placeholders})"
            )

        output_format = self.get_output_format()
        prompt_response_type = _get_genric_arg(output_format.__class__)
        if prompt_response_type != response_type:
            raise TypeError(
                f"{f} response type ({response_type}) does not correspond to prompt output type {prompt_response_type}"
            )

        # todo: validate kwargs against sig.annotations
        # todo: define response parser with validation against response_type

        return LLMRequest(
            messages=self.get_messages(kwargs, template=template),
            response_parser=self.parse,
            response_type=response_type,
        )

    return inner


def _get_genric_arg(cls: Type):
    return typing_inspect.get_args(next(b for b in cls.__orig_bases__ if typing_inspect.is_generic_type(b)))[0]


placeholders_re = re.compile(r"\{([a-zA-Z0-9_]+)}")


class PromptTemplate(EvidentlyBaseModel):
    class Config:
        is_base_type = True

    # __run_func__ : ClassVar[Callable]
    @abstractmethod
    def get_blocks(self) -> Sequence[PromptBlock]:
        raise NotImplementedError

    def iterate(self, values: Sequence[Dict[str, str]]) -> Iterator[str]:
        template = self.get_template()
        for vals in values:
            yield self.render(vals, template)

    def render(self, values: dict, template: Optional[str] = None):
        return (template or self.get_template()).format(**values)

    def get_template(self) -> str:
        return "\n".join(block.render() for block in self.get_blocks())

    def list_placeholders(self, template: Optional[str] = None):
        template = template or self.get_template()
        return list(placeholders_re.findall(template))

    def get_output_format(self) -> OutputFormatBlock:
        output: Optional[OutputFormatBlock] = next(
            (b for b in self.get_blocks() if isinstance(b, OutputFormatBlock)), None
        )
        return output if output is not None else NoopOutputFormat()  # type: ignore[return-value]

    def parse(self, response: str, keys: Optional[List[str]] = None) -> Dict[str, Any]:
        output = self.get_output_format()
        parsed = output.parse_response(response)
        if keys is not None and set(keys) != set(parsed.keys()):
            raise LLMResponseParseError(f"Keys {keys} are required but got {list(parsed.keys())}", response)
        return parsed

    def get_messages(self, values, template: Optional[str] = None) -> List[LLMMessage]:
        return [LLMMessage.user(self.render(values, template))]


class WithSystemPrompt(PromptTemplate, ABC):
    system_prompt: str

    def get_messages(self, values, template: Optional[str] = None) -> List[LLMMessage]:
        msgs = super().get_messages(values, template)
        msgs.insert(0, LLMMessage.system(self.system_prompt))
        return msgs


AnyBlock = Union[str, PromptBlock, Callable]


class BlockPromptTemplate(PromptTemplate):
    class Config:
        type_alias = "evidently:prompt_template:BlockPromptTemplate"

    blocks: ClassVar[List[AnyBlock]]

    def get_blocks(self) -> Sequence[PromptBlock]:
        return [self._to_block(b) for b in self.blocks]

    def _to_block(self, block: AnyBlock) -> PromptBlock:
        if isinstance(block, PromptBlock):
            return block
        if isinstance(block, str):
            return PromptBlock.simple(block)
        # if callable(block):  todo
        #     return PromptBlock.func(block)
        raise NotImplementedError(f"Cannot create promt block from {block}")
