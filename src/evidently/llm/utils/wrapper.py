import asyncio
import dataclasses
import datetime
import json
from abc import ABC
from abc import abstractmethod
from asyncio import Lock
from asyncio import Semaphore
from asyncio import sleep
from importlib.util import find_spec
from typing import Any
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
from evidently.legacy.options.base import Options
from evidently.legacy.options.option import Option
from evidently.legacy.utils.sync import sync_api
from evidently.llm.models import LLMMessage
from evidently.llm.utils.errors import LLMRateLimitError
from evidently.llm.utils.errors import LLMRequestError

TResult = TypeVar("TResult")


class RateLimits(BaseModel):
    rpm: Optional[int] = None
    itpm: Optional[int] = None
    otpm: Optional[int] = None
    tpm: Optional[int] = None
    interval: datetime.timedelta = datetime.timedelta(minutes=1)
    # continious_token_refresh: bool = False


@dataclasses.dataclass
class _Enter:
    ts: datetime.datetime
    estimated_input_tokens: int
    estimated_output_tokens: int
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    done: bool = False

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
        self.enter = _Enter(datetime.datetime.now(), request.estimated_input, 0)

    @property
    def limits(self):
        return self.limiter.limits

    @property
    def enters(self):
        return self.limiter.enters

    @property
    def lock(self):
        return self.limiter.lock

    async def __aenter__(self):
        while True:
            async with self.lock:
                await self.limiter.clean()
                if self._check_rpm() and self._check_tokens():
                    self.enter.ts = datetime.datetime.now()
                    self.enter.estimated_output_tokens = self.limiter.mean_output_size()
                    self.enters.append(self.enter)
                    break
            await sleep(0.1)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        async with self.lock:
            self.enter.done = True
            stat = LimiterStat(
                self.enter.estimated_input_tokens,
                self.enter.estimated_output_tokens,
                self.enter.input_tokens or 0,
                self.enter.output_tokens or 0,
            )
            self.limiter.stats.append(stat)

    def record(self, input_tokens: int, output_tokens: int):
        self.enter.input_tokens = input_tokens
        self.enter.output_tokens = output_tokens

    def _check_rpm(self):
        res = self.limits.rpm is None or len(self.enters) < self.limits.rpm
        return res

    def _check_tokens(self):
        used_input_tokens = 0
        used_output_tokens = 0
        for e in self.enters:
            used_input_tokens += e.input_tokens or e.estimated_input_tokens
            used_output_tokens += e.output_tokens or e.estimated_output_tokens
        input_good = self.limits.itpm is None or used_input_tokens < self.limits.itpm
        output_good = self.limits.otpm is None or used_output_tokens < self.limits.otpm
        total_good = self.limits.tpm is None or used_output_tokens + used_input_tokens < self.limits.tpm
        res = input_good and output_good and total_good
        return res


@dataclasses.dataclass
class LimiterStat:
    estimated_input_tokens: int
    estimated_output_tokens: int
    input_tokens: int
    output_tokens: int


class RateLimiter:
    def __init__(self, limits: RateLimits, initial_output_estimation: int = 100000):
        self.limits = limits
        self.enters: List[_Enter] = []
        self.stats: List[LimiterStat] = []
        self.lock = Lock()
        self.initial_output_estimation = initial_output_estimation

    def enter(self, request: "LimitRequest"):
        return _RateLimiterEntrypoint(self, request)

    async def clean(self):
        now = datetime.datetime.now()
        self.enters = [e for e in self.enters if not e.done or now - e.ts < self.limits.interval]

    def mean_output_size(self):
        if len(self.stats) == 0:
            return self.initial_output_estimation
        return sum(s.output_tokens for s in self.stats) / len(self.stats)


@dataclasses.dataclass
class LLMRequest(Generic[TResult]):
    messages: List[LLMMessage]
    response_parser: Callable[[str], TResult]
    response_type: Type[TResult]
    retries: int = 1


@dataclasses.dataclass
class LLMResult(Generic[TResult]):
    result: TResult
    input_tokens: int
    output_tokens: int


TBatchItem = TypeVar("TBatchItem")
TBatchResult = TypeVar("TBatchResult")


@dataclasses.dataclass
class LimitRequest(Generic[TBatchItem]):
    request: TBatchItem
    estimated_input: int
    # estimated_output: int


class LLMWrapper(ABC):
    __used_options__: ClassVar[List[Type[Option]]] = []

    @abstractmethod
    async def complete(self, messages: List[LLMMessage], seed: Optional[int] = None) -> LLMResult[str]:
        raise NotImplementedError

    async def _batch(
        self,
        coro: Callable[[TBatchItem], Awaitable[LLMResult[TBatchResult]]],
        batches: Sequence[LimitRequest[TBatchItem]],
        batch_size: Optional[int] = None,
        limits: Optional[RateLimits] = None,
    ) -> List[TBatchResult]:
        if batch_size is None:
            batch_size = self.get_batch_size()
        if limits is None:
            limits = self.get_limits()
        rate_limiter = RateLimiter(limits=limits)
        semaphore = Semaphore(batch_size)

        async def work(request: LimitRequest[TBatchItem]) -> TBatchResult:
            async with semaphore, rate_limiter.enter(request) as rate:
                res = await coro(request.request)
                rate.record(res.input_tokens, res.output_tokens)
                return res.result

        return await asyncio.gather(*[work(batch) for batch in batches])

    async def complete_batch(
        self,
        messages_batch: List[List[LLMMessage]],
        batch_size: Optional[int] = None,
        limits: Optional[RateLimits] = None,
    ) -> List[str]:
        requests = [LimitRequest(msgs, sum(self.estimate_tokens(m) for m in msgs)) for msgs in messages_batch]
        return await self._batch(self.complete, requests, batch_size, limits)

    async def run(self, request: LLMRequest[TResult]) -> TResult:
        return (await self._run(request)).result

    async def _run(self, request: LLMRequest[TResult]) -> LLMResult[TResult]:
        num_retries = request.retries
        error = None
        while num_retries >= 0:
            num_retries -= 1
            try:
                response = await self.complete(request.messages)
                return LLMResult(
                    request.response_parser(response.result), response.input_tokens, response.output_tokens
                )
            except Exception as e:
                error = e
        raise error

    async def run_batch(
        self,
        requests: Sequence[LLMRequest[TResult]],
        batch_size: Optional[int] = None,
        limits: Optional[RateLimits] = None,
    ) -> List[TResult]:
        rs = [LimitRequest(r, sum(self.estimate_tokens(m) for m in r.messages)) for r in requests]
        return await self._batch(self._run, rs, batch_size, limits)

    def get_batch_size(self) -> int:
        return 100

    def get_limits(self) -> RateLimits:
        return RateLimits()

    def get_used_options(self) -> List[Type[Option]]:
        return self.__used_options__

    def estimate_tokens(self, msg: LLMMessage):
        return len(msg.content)

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

    class Config:
        extra = "forbid"

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

    def get_additional_kwargs(self) -> Dict[str, Any]:
        return {}


class OpenAIKey(LLMOptions):
    __provider_name__: ClassVar[str] = "openai"
    limits: RateLimits = RateLimits(rpm=500)


OpenAIOptions = OpenAIKey  # for consistency


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

    async def complete(self, messages: List[LLMMessage], seed: Optional[int] = None) -> LLMResult[str]:
        import openai
        from openai.types.chat.chat_completion import ChatCompletion

        messages = [{"role": msg.role, "content": msg.content} for msg in messages]
        try:
            response: ChatCompletion = await self.client.chat.completions.create(
                model=self.model, messages=messages, seed=seed
            )  # type: ignore[arg-type]
        except openai.RateLimitError as e:
            raise LLMRateLimitError(e.message) from e
        except openai.APIError as e:
            raise LLMRequestError(f"Failed to call OpenAI complete API: {e.message}", original_error=e) from e

        content = response.choices[0].message.content
        assert content is not None  # todo: better error
        if response.usage is None:
            return LLMResult(content, 0, 0)
        return LLMResult(content, response.usage.prompt_tokens, response.usage.completion_tokens)

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

    @property
    def provider_and_model(self) -> Tuple[Optional[str], str]:
        if not hasattr(self.options, "__provider_name__"):
            return None, self.model
        provider_name = self.options.__provider_name__
        if self.model.startswith(provider_name + "/"):
            return provider_name, self.model[len(provider_name) + 1 :]
        return provider_name, self.model

    async def complete(self, messages: List[LLMMessage], seed: Optional[int] = None) -> LLMResult[str]:
        from litellm import acompletion
        from litellm.types.utils import ModelResponse
        from litellm.types.utils import Usage

        provider_name, model = self.provider_and_model
        response: ModelResponse = await acompletion(
            model=model,
            custom_llm_provider=provider_name,
            messages=[m.dict() for m in messages],
            api_key=self.options.get_api_key(),
            api_base=self.options.api_url,
            seed=seed,
            **self.options.get_additional_kwargs(),
        )
        content = response.choices[0].message.content
        usage: Optional[Usage] = response.model_extra.get("usage")
        if usage is None:
            return LLMResult(content, 0, 0)
        return LLMResult(content, usage.prompt_tokens, usage.completion_tokens)

    def get_limits(self) -> RateLimits:
        return self.options.limits


class AnthropicOptions(LLMOptions):
    __provider_name__: ClassVar = "anthropic"
    limits: RateLimits = RateLimits(
        rpm=50 // 12, itpm=40000 // 12, otpm=8000 // 12, interval=datetime.timedelta(seconds=5)
    )


@llm_provider("anthropic", None)
class AnthropicWrapper(LiteLLMWrapper):
    __llm_options_type__: ClassVar = AnthropicOptions


class GeminiOptions(LLMOptions):
    __provider_name__: ClassVar = "gemini"


@llm_provider("gemini", None)
class GeminiWrapper(LiteLLMWrapper):
    __llm_options_type__: ClassVar = GeminiOptions


class VertexAIOptions(LLMOptions):
    __provider_name__: ClassVar = "vertex_ai"

    def get_additional_kwargs(self) -> Dict[str, Any]:
        if self.api_key is None or len(self.api_key.get_secret_value()) > 10000:  # check for using non-strict json
            return {}
        try:
            vertex_credentials = json.loads(self.api_key.get_secret_value())
        except json.decoder.JSONDecodeError:
            return {}
        return {"vertex_credentials": vertex_credentials}


@llm_provider("vertex_ai", None)
class VertexAIWrapper(LiteLLMWrapper):
    __llm_options_type__: ClassVar = VertexAIOptions


class DeepSeekOptions(LLMOptions):
    __provider_name__: ClassVar = "deepseek"


@llm_provider("deepseek", None)
class DeepSeekWrapper(LiteLLMWrapper):
    __llm_options_type__: ClassVar = DeepSeekOptions


class MistralOptions(LLMOptions):
    __provider_name__: ClassVar = "mistral"
    limits: RateLimits = RateLimits(rpm=1, itpm=500000 // 60, otpm=500000 // 60, interval=datetime.timedelta(seconds=1))


@llm_provider("mistral", None)
class MistralWrapper(LiteLLMWrapper):
    __llm_options_type__: ClassVar = MistralOptions


class OllamaOptions(LLMOptions):
    __provider_name__: ClassVar = "ollama"
    api_url: str


@llm_provider("ollama", None)
class OllamaWrapper(LiteLLMWrapper):
    __llm_options_type__: ClassVar = OllamaOptions


class NebiusOptions(LLMOptions):
    __provider_name__: ClassVar = "nebius"


@llm_provider("nebius", None)
class NebiusWrapper(LiteLLMWrapper):
    __llm_options_type__: ClassVar = NebiusOptions


excludes = [
    "openai",  # supported natively
    "openai_like",
    "custom_openai",
    "text-completion-openai",
    "anthropic_text",
    "huggingface",  # llama models do not work, disable until tested
    "vertex_ai_beta",
    "azure_text",
    "sagemaker_chat",
    "ollama_chat",
    "text-completion-codestral",
    "watsonx_text",
    "custom",
    "aiohttp_openai",
]
litellm_providers = [
    "openai",
    "openai_like",
    "jina_ai",
    "xai",
    "custom_openai",
    "text-completion-openai",
    "cohere",
    "cohere_chat",
    "clarifai",
    "anthropic",
    "anthropic_text",
    "bytez",
    "replicate",
    "huggingface",
    "together_ai",
    "openrouter",
    "datarobot",
    "vertex_ai",
    "vertex_ai_beta",
    "gemini",
    "ai21",
    "baseten",
    "azure",
    "azure_text",
    "azure_ai",
    "sagemaker",
    "sagemaker_chat",
    "bedrock",
    "vllm",
    "nlp_cloud",
    "petals",
    "oobabooga",
    "ollama",
    "ollama_chat",
    "deepinfra",
    "perplexity",
    "mistral",
    "groq",
    "nvidia_nim",
    "cerebras",
    "ai21_chat",
    "volcengine",
    "codestral",
    "text-completion-codestral",
    "dashscope",
    "deepseek",
    "sambanova",
    "maritalk",
    "voyage",
    "cloudflare",
    "xinference",
    "fireworks_ai",
    "friendliai",
    "featherless_ai",
    "watsonx",
    "watsonx_text",
    "triton",
    "predibase",
    "databricks",
    "empower",
    "github",
    "custom",
    "litellm_proxy",
    "hosted_vllm",
    "llamafile",
    "lm_studio",
    "galadriel",
    "nebius",
    "infinity",
    "deepgram",
    "elevenlabs",
    "novita",
    "aiohttp_openai",
    "langfuse",
    "humanloop",
    "topaz",
    "assemblyai",
    "github_copilot",
    "snowflake",
    "meta_llama",
    "nscale",
]
litellm_providers = [p for p in litellm_providers if p not in excludes]


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
        super(self.__class__, self).__init__(model, options)

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


def main():
    from pprint import pformat

    import litellm

    print(pformat([p.value for p in litellm.provider_list]).replace("'", '"'))


if __name__ == "__main__":
    main()
