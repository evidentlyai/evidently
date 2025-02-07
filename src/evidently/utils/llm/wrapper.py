import asyncio
import dataclasses
import datetime
from abc import ABC
from abc import abstractmethod
from asyncio import Lock
from asyncio import Semaphore
from asyncio import sleep
from importlib.util import find_spec
from typing import Awaitable
from typing import Callable
from typing import ClassVar
from typing import Dict
from typing import Generic
from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Type
from typing import TypeVar

from evidently._pydantic_compat import BaseModel
from evidently._pydantic_compat import SecretStr
from evidently.options.base import Options
from evidently.options.option import Option
from evidently.utils.llm.base import LLMMessage
from evidently.utils.llm.errors import LLMRateLimitError
from evidently.utils.llm.errors import LLMRequestError
from evidently.utils.sync import sync_api

TResult = TypeVar("TResult")


class RateLimits(BaseModel):
    rpm: Optional[int] = None
    itpm: Optional[int] = None
    otpm: Optional[int] = None
    tpm: Optional[int] = None
    continious_token_refresh: bool = False


@dataclasses.dataclass
class _Enter:
    ts: datetime.datetime
    estimated_input_tokens: int
    estimated_output_tokens: int
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None

    @property
    def estimated_tokens(self):
        return self.estimated_input_tokens + self.estimated_output_tokens

    @property
    def tokens(self):
        return self.input_tokens + self.output_tokens


class _RateLimiterEntrypoint:
    def __init__(self, limiter: "RateLimiter", request: "LimitRequest"):
        self.limiter = limiter
        self.request = request

    async def __aenter__(self):
        while True:
            async with self.limiter.lock:
                await self.limiter._clean()
                if self.limiter._check_rpm():
                    self.limiter.enters.append(_Enter(datetime.datetime.now(), 0, 0))
                    break
            await sleep(0.1)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass


class RateLimiter:
    def __init__(self, limits: RateLimits, interval: datetime.timedelta):
        self.limits = limits
        self.interval = interval
        self.enters: List[_Enter] = []
        self.lock = Lock()

    def enter(self, request: "LimitRequest"):
        return _RateLimiterEntrypoint(self, request)

    def _check_rpm(self):
        return self.limits.rpm is None or len(self.enters) < self.limits.rpm

    async def _clean(self):
        now = datetime.datetime.now()
        self.enters = [e for e in self.enters if now - e.ts < self.interval]


@dataclasses.dataclass
class LLMRequest(Generic[TResult]):
    messages: List[LLMMessage]
    response_parser: Callable[[str], TResult]
    response_type: Type[TResult]
    retries: int = 1


TBatchItem = TypeVar("TBatchItem")
TBatchResult = TypeVar("TBatchResult")


@dataclasses.dataclass
class LimitRequest(Generic[TBatchItem]):
    request: TBatchItem


class LLMWrapper(ABC):
    __used_options__: ClassVar[List[Type[Option]]] = []

    @abstractmethod
    async def complete(self, messages: List[LLMMessage]) -> str:
        raise NotImplementedError

    async def _batch(
        self,
        coro: Callable[[TBatchItem], Awaitable[TBatchResult]],
        batches: Sequence[LimitRequest[TBatchItem]],
        batch_size: Optional[int] = None,
        limits: Optional[RateLimits] = None,
    ) -> List[TBatchResult]:
        if batch_size is None:
            batch_size = self.get_batch_size()
        if limits is None:
            limits = self.get_limits()
        rate_limiter = RateLimiter(limits=limits, interval=datetime.timedelta(minutes=1))
        semaphore = Semaphore(batch_size)

        async def work(request: LimitRequest[TBatchItem]) -> TBatchResult:
            async with semaphore, rate_limiter.enter(request):
                return await coro(request.request)

        return await asyncio.gather(*[work(batch) for batch in batches])

    async def complete_batch(
        self,
        messages_batch: List[List[LLMMessage]],
        batch_size: Optional[int] = None,
        limits: Optional[RateLimits] = None,
    ) -> List[str]:
        requests = [LimitRequest(msgs) for msgs in messages_batch]
        return await self._batch(self.complete, requests, batch_size, limits)

    async def run(self, request: LLMRequest[TResult]) -> TResult:
        num_retries = request.retries
        error = None
        while num_retries >= 0:
            num_retries -= 1
            try:
                response = await self.complete(request.messages)
                return request.response_parser(response)
            except Exception as e:
                error = e
        raise error

    async def run_batch(
        self,
        requests: Sequence[LLMRequest[TResult]],
        batch_size: Optional[int] = None,
        limits: Optional[RateLimits] = None,
    ) -> List[TResult]:
        rs = [LimitRequest(r) for r in requests]
        return await self._batch(self.run, rs, batch_size, limits)

    def get_batch_size(self) -> int:
        return 100

    def get_limits(self) -> RateLimits:
        return RateLimits()

    def get_used_options(self) -> List[Type[Option]]:
        return self.__used_options__

    complete_batch_sync = sync_api(complete_batch)
    run_sync = sync_api(run)
    run_batch_sync = sync_api(run_batch)


LLMProvider = str
LLMModel = str
LLMWrapperProvider = Callable[[LLMModel, Options], LLMWrapper]
_wrappers: Dict[Tuple[LLMProvider, Optional[LLMModel]], LLMWrapperProvider] = {}


def llm_provider(name: LLMProvider, model: Optional[LLMModel]) -> Callable[[LLMWrapperProvider], LLMWrapperProvider]:
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
    if find_spec("litellm") is not None:
        litellm_wrapper = get_litellm_wrapper(provider, model, options)
        if litellm_wrapper is not None:
            return litellm_wrapper
    raise ValueError(f"LLM wrapper for provider {provider} model {model} not found. Try installing litellm")


class LLMOptions(Option):
    __provider_name__: ClassVar[str]

    api_key: Optional[SecretStr] = None
    # rpm_limit: int = 500
    limits: RateLimits = RateLimits()
    api_url: Optional[str] = None

    def __init__(self, api_key: Optional[str] = None, rpm_limit: Optional[int] = None, **data):
        self.api_key = SecretStr(api_key) if api_key is not None else None
        super().__init__(**data)
        # backward comp
        if rpm_limit is not None:
            self.limits.rpm = rpm_limit

    def get_api_key(self) -> Optional[str]:
        if self.api_key is None:
            return None
        return self.api_key.get_secret_value()


class OpenAIKey(LLMOptions):
    __provider_name__: ClassVar[str] = "openai"
    limits: RateLimits = RateLimits(rpm=500)


@llm_provider("openai", None)
class OpenAIWrapper(LLMWrapper):
    __used_options__: ClassVar = [OpenAIKey]

    def __init__(self, model: str, options: Options):
        import openai

        self.model = model
        self.options = options.get(OpenAIKey)
        self._clients: Dict[int, openai.AsyncOpenAI] = {}

    @property
    def client(self):
        import openai

        try:
            loop = asyncio.get_running_loop()
        except RuntimeError as e:
            raise RuntimeError("Cannot access OpenAIWrapper client without loop") from e
        loop_id = id(loop)
        if loop_id not in self._clients:
            self._clients[loop_id] = openai.AsyncOpenAI(
                api_key=self.options.get_api_key(), base_url=self.options.api_url
            )
        return self._clients[loop_id]

    async def complete(self, messages: List[LLMMessage]) -> str:
        import openai

        messages = [{"role": msg.role, "content": msg.content} for msg in messages]
        try:
            response = await self.client.chat.completions.create(model=self.model, messages=messages)  # type: ignore[arg-type]
        except openai.RateLimitError as e:
            raise LLMRateLimitError(e.message) from e
        except openai.APIError as e:
            raise LLMRequestError(f"Failed to call OpenAI complete API: {e.message}", original_error=e) from e

        content = response.choices[0].message.content
        assert content is not None  # todo: better error
        return content

    def get_limits(self) -> RateLimits:
        return self.options.limits


def get_litellm_wrapper(provider: LLMProvider, model: LLMModel, options: Options) -> Optional[LLMWrapper]:
    from litellm import BadRequestError
    from litellm.litellm_core_utils.get_llm_provider_logic import get_llm_provider

    try:
        model, provider, *_ = get_llm_provider(model, provider)
        return LiteLLMWrapper(f"{provider}/{model}", options)
    except BadRequestError:
        return None


@llm_provider("litellm", None)
class LiteLLMWrapper(LLMWrapper):
    __llm_options_type__: ClassVar[Type[LLMOptions]] = LLMOptions

    def get_used_options(self) -> List[Type[Option]]:
        return [self.__llm_options_type__]

    def __init__(self, model: str, options: Options):
        self.model = model
        self.options: LLMOptions = options.get(self.__llm_options_type__)

    async def complete(self, messages: List[LLMMessage]) -> str:
        from litellm import acompletion

        return (
            (
                await acompletion(
                    model=self.model,
                    messages=[dataclasses.asdict(m) for m in messages],
                    api_key=self.options.get_api_key(),
                    api_base=self.options.api_url,
                )
            )
            .choices[0]
            .message.content
        )

    def get_limits(self) -> RateLimits:
        return self.options.limits


class AnthropicOptions(LLMOptions):
    __provider_name__: ClassVar = "anthropic"
    limits: RateLimits = RateLimits(rpm=50)


@llm_provider("anthropic", None)
class AnthropicWrapper(LiteLLMWrapper):
    __llm_options_type__: ClassVar = AnthropicOptions


class GeminiOptions(LLMOptions):
    __provider_name__: ClassVar = "gemini"


@llm_provider("gemini", None)
class GeminiWrapper(LiteLLMWrapper):
    __llm_options_type__: ClassVar = GeminiOptions


class DeepSeekOptions(LLMOptions):
    __provider_name__: ClassVar = "deepseek"


@llm_provider("deepseek", None)
class DeepSeekWrapper(LiteLLMWrapper):
    __llm_options_type__: ClassVar = DeepSeekOptions


litellm_providers = [
    # 'openai', # supported natively
    # 'openai_like',
    "jina_ai",
    "xai",
    # 'custom_openai',
    # 'text-completion-openai',
    "cohere",
    "cohere_chat",
    "clarifai",
    "anthropic",
    # 'anthropic_text',
    "replicate",
    # "huggingface",  # llama models do not work, disable until tested
    "together_ai",
    "openrouter",
    "vertex_ai",
    # 'vertex_ai_beta',
    "gemini",
    "ai21",
    "baseten",
    "azure",
    # 'azure_text',
    "azure_ai",
    "sagemaker",
    # 'sagemaker_chat',
    "bedrock",
    "vllm",
    "nlp_cloud",
    "petals",
    "oobabooga",
    "ollama",
    # 'ollama_chat',
    "deepinfra",
    "perplexity",
    "mistral",
    "groq",
    "nvidia_nim",
    "cerebras",
    "ai21_chat",
    "volcengine",
    "codestral",
    # 'text-completion-codestral',
    "deepseek",
    "sambanova",
    "maritalk",
    "voyage",
    "cloudflare",
    "xinference",
    "fireworks_ai",
    "friendliai",
    "watsonx",
    # 'watsonx_text',
    "triton",
    "predibase",
    "databricks",
    "empower",
    "github",
    # 'custom',
    "litellm_proxy",
    "hosted_vllm",
    "lm_studio",
    "galadriel",
    "infinity",
    "deepgram",
    # 'aiohttp_openai',
    "langfuse",
    "humanloop",
    "topaz",
]


def _create_litellm_wrapper(provider: str):
    words = provider.split("_")
    class_name_prefix = "".join(word.upper() if word.lower() == "ai" else word.capitalize() for word in words)

    wrapper_name = f"{class_name_prefix}Wrapper"
    options_name = f"{class_name_prefix}Options"
    options_type = type(
        options_name,
        (LLMOptions,),
        {"__provider_name__": provider, "__annotations__": {"__provider_name__": ClassVar[str]}},
    )

    def __init__(self, model: str, options: Options):
        super(self.__class__, self).__init__(f"{provider}/{model}", options)

    wrapper_type = type(
        wrapper_name,
        (LiteLLMWrapper,),
        {
            "__llm_options_type__": options_type,
            "__annotations__": {"__llm_options_type__": ClassVar},
            "__init__": __init__,
        },
    )

    return {
        wrapper_name: llm_provider(provider, None)(wrapper_type),
        options_name: options_type,
    }


for provider in litellm_providers:
    key = (provider, None)
    if key in _wrappers:
        continue
    locals().update(**_create_litellm_wrapper(provider))
