import asyncio
import dataclasses
import datetime
import json
from abc import ABC
from abc import abstractmethod
from asyncio import Lock
from asyncio import Semaphore
from asyncio import sleep
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

from evidently._pydantic_compat import SecretStr
from evidently.errors import EvidentlyError
from evidently.options.base import Options
from evidently.options.option import Option
from evidently.pydantic_utils import EvidentlyBaseModel
from evidently.ui.base import sync_api


@dataclasses.dataclass
class LLMMessage:
    role: str
    content: str

    @classmethod
    def user(cls, message: str):
        return LLMMessage("user", message)

    @classmethod
    def system(cls, message: str):
        return LLMMessage("system", message)


LLMResponse = Dict[str, Any]


class EvidentlyLLMError(EvidentlyError):
    pass


class LLMResponseParseError(EvidentlyLLMError):
    pass


class LLMRequestError(EvidentlyLLMError):
    pass


class RateLimiter:
    def __init__(self, rate: Optional[int], interval: datetime.timedelta):
        self.rate = rate
        self.interval = interval
        self.enters = []
        self.lock = Lock()

    async def __aenter__(self):
        if self.rate is None:
            return
        while True:
            async with self.lock:
                await self._clean()
                if len(self.enters) < self.rate:
                    self.enters.append(datetime.datetime.now())
                    break
            await sleep(0.1)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def _clean(self):
        now = datetime.datetime.now()
        self.enters = [e for e in self.enters if now - e < self.interval]


class LLMWrapper(ABC):
    __used_options__: ClassVar[List[Type[Option]]] = []

    @abstractmethod
    async def complete(self, messages: List[LLMMessage]) -> str:
        raise NotImplementedError

    async def batch_complete(
        self, messages_batch: List[List[LLMMessage]], batch_size: Optional[int] = None, rpm_limit: Optional[int] = None
    ) -> List[str]:
        if batch_size is None:
            batch_size = self.get_batch_size()
        if rpm_limit is None:
            rpm_limit = self.get_rpm_limit()
        rate_limiter = RateLimiter(rate=rpm_limit, interval=datetime.timedelta(minutes=1))
        semaphore = Semaphore(batch_size)

        async def work(messages: List[LLMMessage]) -> str:
            async with semaphore, rate_limiter:
                return await self.complete(messages)

        return await asyncio.gather(*[work(msgs) for msgs in messages_batch])

    batch_complete_sync = sync_api(batch_complete)

    def get_batch_size(self) -> int:
        return 100

    def get_rpm_limit(self) -> Optional[int]:
        return None

    def get_used_options(self) -> List[Type[Option]]:
        return self.__used_options__


LLMProvider = str
LLMModel = str
LLMWrapperProvider = Callable[[LLMModel, Options], LLMWrapper]
_wrappers: Dict[Tuple[LLMProvider, Optional[LLMModel]], LLMWrapperProvider] = {}


def llm_provider(name: LLMProvider, model: Optional[LLMModel]):
    def dec(f: LLMWrapperProvider):
        _wrappers[(name, model)] = f
        return f

    return dec


def get_llm_wrapper(provider: LLMProvider, model: LLMModel, options: Options) -> LLMWrapper:
    key: Tuple[str, Optional[str]] = (provider, model)
    if key in _wrappers:
        return _wrappers[key](model, options)
    key = (provider, None)
    if key in _wrappers:
        return _wrappers[key](model, options)
    raise ValueError(f"LLM wrapper for provider {provider} model {model} not found")


class OpenAIKey(Option):
    api_key: Optional[SecretStr] = None
    rpm_limit: int = 500

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = SecretStr(api_key) if api_key is not None else None
        super().__init__()

    def get_api_key(self) -> Optional[str]:
        if self.api_key is None:
            return None
        return self.api_key.get_secret_value()


@llm_provider("openai", None)
class OpenAIWrapper(LLMWrapper):
    __used_options__: ClassVar = [OpenAIKey]

    def __init__(self, model: str, options: Options):
        self.model = model
        self.options = options.get(OpenAIKey)
        self._clients = {}

    @property
    def client(self):
        import openai

        try:
            loop = asyncio.get_running_loop()
        except RuntimeError as e:
            raise RuntimeError("Cannot access OpenAIWrapper client without loop") from e
        loop_id = id(loop)
        if loop_id not in self._clients:
            self._clients[loop_id] = openai.AsyncOpenAI(api_key=self.options.get_api_key())
        return self._clients[loop_id]

    async def complete(self, messages: List[LLMMessage]) -> str:
        import openai

        messages = [{"role": msg.role, "content": msg.content} for msg in messages]
        try:
            response = await self.client.chat.completions.create(model=self.model, messages=messages)  # type: ignore[arg-type]
        except openai.OpenAIError as e:
            raise LLMRequestError("Failed to call OpenAI complete API") from e
        content = response.choices[0].message.content
        assert content is not None  # todo: better error
        return content

    def get_rpm_limit(self) -> Optional[int]:
        return self.options.rpm_limit


@llm_provider("litellm", None)
class LiteLLMWrapper(LLMWrapper):
    def __init__(self, model: str):
        self.model = model

    def complete(self, messages: List[LLMMessage]) -> str:
        from litellm import completion

        return completion(model=self.model, messages=messages).choices[0].message.content


class PromptBlock(EvidentlyBaseModel):
    class Config:
        alias_required = False  # fixme

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


class OutputFormatBlock(PromptBlock, ABC):
    @abstractmethod
    def parse_response(self, response: str) -> Dict[str, str]:
        raise NotImplementedError


class JsonOutputFormatBlock(OutputFormatBlock):
    fields: Dict[str, Union[Tuple[str, str], str]]

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

    def parse_response(self, response: str) -> Dict[str, str]:
        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            raise LLMResponseParseError(f"Failed to parse response '{response}' as json") from e


class StringListFormatBlock(OutputFormatBlock):
    of_what: str

    def _render(self) -> str:
        return f"""Return a list of {self.of_what}.
This should be only a list of string {self.of_what}, each one on a new line with no enumeration"""

    def parse_response(self, response: str) -> Dict[str, str]:
        return {self.of_what: response.split("\n")}


class StringFormatBlock(OutputFormatBlock):
    what: str

    def _render(self) -> str:
        return f"""Return {self.what} only."""

    def parse_response(self, response: str) -> Dict[str, str]:
        return {self.what: response}


class PromptTemplate(EvidentlyBaseModel):
    class Config:
        alias_required = False  # fixme

    @abstractmethod
    def get_blocks(self) -> Sequence[PromptBlock]:
        raise NotImplementedError

    def iterate(self, values: Sequence[Dict[str, str]]) -> Iterator[str]:
        template = self.get_template()
        for vals in values:
            yield template.format(**vals)

    def render(self, **values):
        return self.get_template().format(**values)

    def get_template(self) -> str:
        return "\n".join(block.render() for block in self.get_blocks())

    def parse(self, response: str, keys: Optional[List[str]] = None) -> Dict[str, Any]:
        output = next((b for b in self.get_blocks() if isinstance(b, OutputFormatBlock)), None)
        if output is None:
            return {"": response}
        parsed = output.parse_response(response)
        if keys is not None and set(keys) != set(parsed.keys()):
            raise LLMResponseParseError(f"Keys {keys} are required but got {list(parsed.keys())}")
        return parsed


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
        if callable(block):
            return PromptBlock.func(block)
        raise NotImplementedError(f"Cannot create promt block from {block}")


# class BinaryClassificationPromtTemplate(PromptTemplate):
#     def get_blocks(self) -> Sequence[PromptBlock]:
#         fields = {}
#         if self.include_category:
#             cat = f"{self.target_category} or {self.non_target_category}"
#             if self.uncertainty == Uncertainty.UNKNOWN:
#                 cat += " or UNKNOWN"
#             fields["category"] = (cat, self.output_column)
#         if self.include_score:
#             fields["score"] = ("<score here>", self.output_score_column)
#         if self.include_reasoning:
#             fields["reasoning"] = ('"<reasoning here>"', self.output_reasoning_column)
#         return [
#             PromptBlock.simple(self.criteria),
#             PromptBlock.simple(
#                 f"Classify text between {self.anchor_start} and {self.anchor_end} "
#                 f"into two categories: {self.target_category} and {self.non_target_category}."
#             ),
#             PromptBlock.input().anchored(self.anchor_start, self.anchor_end),
#             PromptBlock.func(self._instructions),
#             JsonOutputFormatBlock(fields=fields),
#         ]
#
#     criteria: str = ""
#     instructions_template: str = (
#         "Use the following categories for classification:\n{__categories__}\n{__scoring__}\nThink step by step."
#     )
#     anchor_start: str = "___text_starts_here___"
#     anchor_end: str = "___text_ends_here___"
#
#     placeholders: Dict[str, str] = {}
#     target_category: str
#     non_target_category: str
#
#     uncertainty: Uncertainty = Uncertainty.UNKNOWN
#
#     include_category: bool = True
#     include_reasoning: bool = False
#     include_score: bool = False
#     score_range: Tuple[float, float] = (0.0, 1.0)
#
#     output_column: str = "category"
#     output_reasoning_column: str = "reasoning"
#     output_score_column: str = "score"
#
#     pre_messages: List[LLMMessage] = Field(default_factory=list)