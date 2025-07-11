import ast
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

from evidently.llm.models import LLMMessage
from evidently.llm.utils.errors import LLMResponseParseError
from evidently.llm.utils.wrapper import LLMRequest
from evidently.pydantic_utils import AutoAliasMixin
from evidently.pydantic_utils import EvidentlyBaseModel

TResult = TypeVar("TResult")


class PromptBlock(AutoAliasMixin, EvidentlyBaseModel):
    __alias_type__: ClassVar[str] = "prompt_block"

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
    start: str
    block: PromptBlock
    end: str

    def _render(self) -> str:
        return f"{self.start}\n{self.block.render()}\n{self.end}"


class SimpleBlock(PromptBlock):
    value: str

    def _render(self) -> str:
        return self.value


class CompositePromptBlock(PromptBlock):
    def _render(self) -> str:
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


class OutputFormatBlock(PromptBlock, ABC, Generic[TResult]):
    @abstractmethod
    def parse_response(self, response: str) -> TResult:
        raise NotImplementedError


class NoopOutputFormat(OutputFormatBlock[str]):
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
    of_what: str

    def _render(self) -> str:
        return f"""Return a list of {self.of_what}.
This should be only a list of string {self.of_what}, each one on a new line with no enumeration"""

    def parse_response(self, response: str) -> List[str]:
        return [line.strip() for line in response.split("\n") if line.strip()]


class StringFormatBlock(OutputFormatBlock[str]):
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


class PromptTemplate(AutoAliasMixin, EvidentlyBaseModel):
    __alias_type__: ClassVar = "prompt_template"

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
        raise NotImplementedError(f"Cannot create prompt block from {block}")


def prompt_contract(f: Callable):
    from evidently.legacy.utils.llm.prompts import llm_call

    res = llm_call(f)
    res.__llm_call__ = True  # type: ignore[attr-defined]
    res.__original__ = f  # type: ignore[attr-defined]
    return res


def _parse_function_call(call_string) -> Tuple[str, List, Dict, bool]:
    try:
        node = ast.parse(call_string, mode="eval").body
    except SyntaxError:
        raise ValueError("Invalid function call syntax")

    if not isinstance(node, ast.Call):
        raise ValueError("The string is not a valid function call")

    if isinstance(node.func, ast.Name):
        is_method = False
        func_name = node.func.id
    elif isinstance(node.func, ast.Attribute):
        is_method = True
        func_name = node.func.attr
    else:
        raise ValueError("Unsupported function call format")

    args = [arg.id for arg in node.args]
    kwargs = {kw.arg: ast.literal_eval(kw.value) for kw in node.keywords}

    return func_name, args, kwargs, is_method


PromptCommandCallable = Callable[..., PromptBlock]
_prompt_command_registry: Dict[str, PromptCommandCallable] = {
    "output_json": PromptBlock.json_output,
    "output_string_list": PromptBlock.string_list_output,
    "output_string": PromptBlock.string_output,
}


def prompt_command(f: Union[str, PromptCommandCallable]):
    name = f if isinstance(f, str) else f.__name__

    def dec(func: PromptCommandCallable):
        _prompt_command_registry[name] = func
        return func

    return dec(f) if callable(f) else dec


@prompt_command("input")
def prompt_block_input(
    placeholder_name: str = "input", anchors: bool = False, start: str = "__start__", end: str = "__end__"
):
    res = PromptBlock.input(placeholder_name)
    if anchors:
        res = res.anchored(start, end)
    return res


_self_placeholder_re = re.compile(r"{self\.([a-zA-Z_][a-zA-Z0-9_]*)}")


def replace_self_placeholders(prompt: str, self_obj: Any):
    def repl(match):
        attr_name = match.group(1)
        value = getattr(self_obj, attr_name, match.group(0))  # keep placeholder if attr missing
        if isinstance(value, PromptBlock):
            return value.render()
        return str(value)

    return _self_placeholder_re.sub(repl, prompt)


class StrPromptTemplate(PromptTemplate):
    prompt_template: Optional[str] = None
    _contract: ClassVar[Callable]

    def __init_subclass__(cls):
        super().__init_subclass__()
        contract = None
        for value in cls.__dict__.values():
            if callable(value) and getattr(value, "__llm_call__", None):
                contract = value
        if contract is not None:
            cls._contract = contract

    def _get_prompt_template(self):
        pt = self.prompt_template or self._contract.__doc__
        if pt is None:
            raise ValueError("Prompt template is not provided and contract function __doc__ is empty")
        return pt

    def get_blocks(self) -> Sequence[PromptBlock]:
        prompt_template = self._get_prompt_template()
        return self._template_to_blocks(prompt_template)

    def _template_to_blocks(self, prompt_template: str) -> List[PromptBlock]:
        res = []
        for part in re.split(r"({%\s.*?\s%})", prompt_template):
            if not part.startswith("{%"):
                part = replace_self_placeholders(part, self)
                res.append(PromptBlock.simple(part))
                continue
            cmd = part.strip("{}% ")
            res.extend(
                b if isinstance(b, PromptBlock) else PromptBlock.simple(b) for b in self._parse_cmd_to_blocks(cmd)
            )

        return res

    def _find_parent_contract(self) -> Tuple[Type["StrPromptTemplate"], Callable]:
        if self._contract is None:
            raise ValueError("super() only available in @prompt_contract methods")
        for parent in self.__class__.mro():
            if parent is self.__class__:
                continue
            if not isinstance(parent, type) or not issubclass(parent, StrPromptTemplate):
                continue
            if not hasattr(parent, "_contract"):
                continue
            return parent, parent._contract
        raise ValueError("No parent contract found")

    def _parse_cmd_to_blocks(self, cmd: str) -> List[Union[PromptBlock, str]]:
        func_name, args, kwargs, is_method = _parse_function_call(cmd)
        if is_method:
            func = getattr(self, func_name)
            return [func(*args, **kwargs)]
        if func_name == "super":
            parent, contract = self._find_parent_contract()
            return parent._template_to_blocks(self, contract.__doc__)
        if func_name not in _prompt_command_registry:
            raise ValueError(
                f"Unknown function call `{func_name}`. Available functions: {list(_prompt_command_registry.keys())}"
            )
        return [_prompt_command_registry[func_name](*args, **kwargs)]

    def _validate_prompt_template(self):
        # todo: deduplicate with @llm_call.inner
        template = self.get_template()
        placeholders = self.list_placeholders(template)
        sig = inspect.getfullargspec(self._contract.__original__)
        arg_names = set(sig.args).difference(["self"])
        if set(placeholders) != arg_names:
            raise ValueError(
                f"Wrong prompt template: {self.__class__._contract} signature has {arg_names} args, "
                f"but prompt has {placeholders} placeholders"
            )
        response_type = sig.annotations.get("return", str)

        output_format = self.get_output_format()
        prompt_response_type = _get_genric_arg(output_format.__class__)
        if prompt_response_type != response_type:
            raise TypeError(
                f"Response type ({response_type}) does not correspond to prompt output type {prompt_response_type}"
            )

    @classmethod
    def compile(cls, prompt_template: str, **kwargs):
        res = cls(prompt_template=prompt_template, **kwargs)
        res._validate_prompt_template()
        return res
