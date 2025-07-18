import contextlib
import inspect
import itertools
import textwrap
from abc import ABC
from abc import abstractmethod
from functools import wraps
from typing import Any
from typing import Callable
from typing import ClassVar
from typing import Dict
from typing import Iterator
from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Type
from typing import Union
from typing import get_args

import typing_inspect
from typing_inspect import is_classvar

from evidently._pydantic_compat import PrivateAttr
from evidently.llm.models import LLMMessage
from evidently.llm.utils.blocks import OutputFormatBlock
from evidently.llm.utils.blocks import PromptBlock
from evidently.llm.utils.errors import LLMResponseParseError
from evidently.llm.utils.prompt_render import PreparedTemplate
from evidently.llm.utils.prompt_render import TemplateRenderer
from evidently.llm.utils.prompt_render import prompt_command
from evidently.llm.utils.wrapper import LLMRequest
from evidently.pydantic_utils import AutoAliasMixin
from evidently.pydantic_utils import EvidentlyBaseModel


def llm_call(f: Callable) -> Callable[..., LLMRequest]:
    sig = inspect.getfullargspec(f)
    response_type = sig.annotations.get("return", str)

    @wraps(f)
    def inner(self: PromptTemplate, *args, **kwargs):
        kwargs = inspect.getcallargs(f, *args, **kwargs, self=self)
        del kwargs["self"]
        placeholders = self.list_placeholders()
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
            messages=self.get_messages(kwargs),
            response_parser=self.get_parser(),
            response_type=response_type,
        )

    return inner


def _get_genric_arg(cls: Type):
    return typing_inspect.get_args(next(b for b in cls.__orig_bases__ if typing_inspect.is_generic_type(b)))[0]


class PromptTemplate(AutoAliasMixin, EvidentlyBaseModel):
    __alias_type__: ClassVar = "prompt_template"
    _prepared_template: PreparedTemplate = PrivateAttr()

    class Config:
        is_base_type = True

    def render(self, values: dict) -> str:
        return self.prepared_template.render(values)

    def iterate(self, values: Sequence[Dict[str, str]]) -> Iterator[str]:
        for vals in values:
            yield self.render(vals)

    @abstractmethod
    def prepare(self) -> PreparedTemplate:
        raise NotImplementedError()

    @property
    def prepared_template(self) -> PreparedTemplate:
        if not hasattr(self, "_prepared_template"):
            self._prepared_template = self.prepare()
        return self._prepared_template

    def clear_prepared_template(self):
        try:
            delattr(self, "_prepared_template")
        except AttributeError:
            pass

    def list_placeholders(self):
        return self.prepared_template.placeholders

    def get_output_format(self) -> OutputFormatBlock:
        return self.prepared_template.output_format

    def get_parser(self):
        output = self.get_output_format()

        def parse(response: str, keys: Optional[List[str]] = None) -> Dict[str, Any]:
            parsed = output.parse_response(response)
            if keys is not None and set(keys) != set(parsed.keys()):
                raise LLMResponseParseError(f"Keys {keys} are required but got {list(parsed.keys())}", response)
            return parsed

        return parse

    def get_messages(self, values) -> List[LLMMessage]:
        return [LLMMessage.user(self.render(values))]


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

    def prepare(self) -> PreparedTemplate:
        blocks = self.get_blocks()
        output: Optional[OutputFormatBlock] = next((b for b in blocks if isinstance(b, OutputFormatBlock)), None)
        return PreparedTemplate("\n".join(block.render() for block in blocks), output_format=output)


class WithSystemPrompt(PromptTemplate, ABC):
    system_prompt: str

    def get_messages(self, values) -> List[LLMMessage]:
        msgs = super().get_messages(values)
        msgs.insert(0, LLMMessage.system(self.system_prompt))
        return msgs


def prompt_contract(f: Callable):
    res = llm_call(f)
    res.__llm_call__ = True  # type: ignore[attr-defined]
    res.__original__ = f  # type: ignore[attr-defined]
    return res


@prompt_command("input")
def prompt_block_input(placeholder_name: str = "input", tag: bool = False, anchors: bool = False):
    res = PromptBlock.input(placeholder_name)
    if tag or anchors:
        res = res.tag(placeholder_name)
    return res


def smart_isinstance(value, type_) -> bool:
    if isinstance(type_, type):
        return isinstance(value, type_)
    generic_type = typing_inspect.get_origin(type_)
    subtype = typing_inspect.get_args(type_)[0]
    if generic_type is list:
        return isinstance(value, list) and all(isinstance(v, subtype) for v in value)
    raise NotImplementedError(f"Not implemented for {type_}")


class StrPromptTemplate(PromptTemplate):
    prompt_template: Optional[str] = None
    _contract: ClassVar[Callable]
    _context_vars: Dict[str, Any] = PrivateAttr()

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
        return textwrap.dedent(pt)

    def list_context_variables(self) -> Dict[str, Type]:
        return {name: get_args(ann)[-1] for name, ann in self.__class__.__annotations__.items() if is_classvar(ann)}

    def _set_context_variable(self, name: str, value: Any):
        context_vars = self._get_context_variables()
        context_vars[name] = value
        self._context_vars = context_vars

    def _set_context_variables(self, variables: Dict[str, Any]):
        self._context_vars = variables

    def _get_context_variables(self) -> Dict[str, Any]:
        if not hasattr(self, "_context_vars"):
            return {}
        return self._context_vars

    def _delete_context_variables(self):
        delattr(self, "_context_vars")

    @contextlib.contextmanager
    def with_context(self, **variables: Any):
        old_vars = self._get_context_variables()
        try:
            self._set_context_variables(variables)
            yield
        finally:
            self._set_context_variables(old_vars)
            self.clear_prepared_template()

    def _validate_context_variables(self):
        expected_vars = self.list_context_variables()
        variables = self._get_context_variables()
        errors = []
        template = self._get_prompt_template()
        for name, type_ in expected_vars.items():
            if f"{{{name}}}" not in template:
                continue
            if name not in variables:
                errors.append(f"'{name}' context variable is not provided")
                continue
            if not smart_isinstance(variables[name], type_):
                errors.append(f"Variable '{name}' context variable is not of type '{type_}'")
        if errors:
            raise ValueError("\n".join(errors))
        return variables

    def prepare(self, **variables: Any) -> PreparedTemplate:
        if len(variables) > 0:
            with self.with_context(**variables):
                variables = self._validate_context_variables()
                return self._prepare(self._get_prompt_template(), variables, self)
        variables = self._validate_context_variables()
        return self._prepare(self._get_prompt_template(), variables, self)

    @staticmethod
    def _prepare(template: str, variables, self) -> PreparedTemplate:
        renderer = TemplateRenderer(template, self)
        for name, value in variables.items():
            renderer.add_var(name, value)
        renderer.add_command("super", self._get_super_block)
        return renderer.prepare()

    def _get_super_block(self) -> List[PromptBlock]:
        parent, contract = self._find_parent_contract()
        doc = contract.__doc__
        if doc is None:
            raise ValueError("'super()' can't find parent prompt_contract")
        prepare = self._prepare(doc, self._get_context_variables(), self)
        if prepare.has_output_format:
            of = prepare.output_format
            parts = prepare.template.split(of.render())
            return list(itertools.chain.from_iterable(([of, PromptBlock.simple(part)] for part in parts)))[1:]
        return [PromptBlock.simple(prepare.template)]

    def get_output_format(self) -> OutputFormatBlock:
        return self.prepared_template.output_format

    def _validate_prompt_template(self):
        # todo: deduplicate with @llm_call.inner
        placeholders = self.list_placeholders()
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

    def _find_parent_contract(self) -> Tuple[Type["StrPromptTemplate"], Callable]:
        for parent in self.__class__.mro():
            if parent is self.__class__ and self.prompt_template is None:
                continue
            if not isinstance(parent, type) or not issubclass(parent, StrPromptTemplate):
                continue
            if not hasattr(parent, "_contract"):
                continue
            return parent, parent._contract
        raise ValueError("No parent contract found")

    @classmethod
    def compile(cls, prompt_template: str, context_vars: Optional[Dict[str, Any]] = None, **kwargs):
        res = cls(prompt_template=prompt_template, **kwargs)
        with res.with_context(**(context_vars or {})):
            res._validate_prompt_template()
        return res


def main():
    class MyTemplate(StrPromptTemplate):
        @prompt_contract
        def lol(self, a: str):
            """a: {a}
            {% output_string_list(qqq, tagged=True) %}
            """

    other_template = MyTemplate(prompt_template="lol\n{% super() %}")
    print(other_template.prepared_template)

    print(f"__{other_template.prepared_template.output_format.__class__.__name__}__")
    print(f"__{MyTemplate().prepared_template.output_format.__class__.__name__}__")

    class MyTemplate2(MyTemplate):
        @prompt_contract
        def lol(self, a: str):
            """kek
            {% super() %}
            """

    print(MyTemplate2().prepared_template)
    print(f"__{MyTemplate2().prepared_template.output_format.__class__.__name__}__")


if __name__ == "__main__":
    main()
