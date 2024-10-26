import asyncio
import dataclasses
import datetime
from abc import ABC
from abc import abstractmethod
from asyncio import Lock
from asyncio import Semaphore
from asyncio import sleep
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

from evidently._pydantic_compat import SecretStr
from evidently.options.base import Options
from evidently.options.option import Option
from evidently.utils.llm.base import LLMMessage
from evidently.utils.llm.errors import LLMRequestError
from evidently.utils.sync import sync_api

TResult = TypeVar("TResult")


class RateLimiter:
    def __init__(self, rate: Optional[int], interval: datetime.timedelta):
        self.rate = rate
        self.interval = interval
        self.enters: List[datetime.datetime] = []
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


@dataclasses.dataclass
class LLMRequest(Generic[TResult]):
    messages: List[LLMMessage]
    response_parser: Callable[[str], TResult]
    response_type: Type[TResult]
    retries: int = 1


class LLMWrapper(ABC):
    __used_options__: ClassVar[List[Type[Option]]] = []

    @abstractmethod
    async def complete(self, messages: List[LLMMessage]) -> str:
        raise NotImplementedError

    async def complete_batch(
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
        self, requests: Sequence[LLMRequest[TResult]], batch_size: Optional[int] = None, rpm_limit: Optional[int] = None
    ) -> List[TResult]:
        if batch_size is None:
            batch_size = self.get_batch_size()
        if rpm_limit is None:
            rpm_limit = self.get_rpm_limit()
        rate_limiter = RateLimiter(rate=rpm_limit, interval=datetime.timedelta(minutes=1))
        semaphore = Semaphore(batch_size)

        async def work(request: LLMRequest[TResult]) -> TResult:
            async with semaphore, rate_limiter:
                return await self.run(request)

        return await asyncio.gather(*[work(r) for r in requests])

    def get_batch_size(self) -> int:
        return 100

    def get_rpm_limit(self) -> Optional[int]:
        return None

    def get_used_options(self) -> List[Type[Option]]:
        return self.__used_options__

    complete_batch_sync = sync_api(complete_batch)
    run_sync = sync_api(run)
    run_batch_sync = sync_api(run_batch)


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
            self._clients[loop_id] = openai.AsyncOpenAI(api_key=self.options.get_api_key())
        return self._clients[loop_id]

    async def complete(self, messages: List[LLMMessage]) -> str:
        import openai

        messages = [{"role": msg.role, "content": msg.content} for msg in messages]
        try:
            response = await self.client.chat.completions.create(model=self.model, messages=messages)  # type: ignore[arg-type]
        except openai.APIError as e:
            raise LLMRequestError(f"Failed to call OpenAI complete API: {e.message}") from e
        content = response.choices[0].message.content
        assert content is not None  # todo: better error
        return content

    def get_rpm_limit(self) -> Optional[int]:
        return self.options.rpm_limit


@llm_provider("litellm", None)
class LiteLLMWrapper(LLMWrapper):
    def __init__(self, model: str):
        self.model = model

    async def complete(self, messages: List[LLMMessage]) -> str:
        from litellm import completion

        return completion(model=self.model, messages=messages).choices[0].message.content
