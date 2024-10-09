from abc import ABC
from abc import abstractmethod
from typing import Callable
from typing import ClassVar
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Type
from typing import Union

from evidently._pydantic_compat import PrivateAttr
from evidently._pydantic_compat import SecretStr
from evidently.errors import EvidentlyError
from evidently.options.base import Options
from evidently.options.option import Option

LLMMessage = Tuple[str, str]
LLMResponse = Dict[str, Union[str, float]]


class EvidentlyLLMError(EvidentlyError):
    pass


class LLMResponseParseError(EvidentlyLLMError):
    pass


class LLMRequestError(EvidentlyLLMError):
    pass


class LLMWrapper(ABC):
    __used_options__: ClassVar[List[Type[Option]]] = []

    @abstractmethod
    def complete(self, messages: List[LLMMessage]) -> str:
        raise NotImplementedError

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


class WithLLMWrapper:
    provider: str
    model: str
    _llm_wrapper: Optional[LLMWrapper] = PrivateAttr(None)

    def get_llm_wrapper(self, options: Options) -> LLMWrapper:
        if self._llm_wrapper is None:
            self._llm_wrapper = get_llm_wrapper(self.provider, self.model, options)
        return self._llm_wrapper


class OpenAIKey(Option):
    api_key: Optional[SecretStr] = None

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = SecretStr(api_key) if api_key is not None else None
        super().__init__()

    def get_value(self) -> Optional[str]:
        if self.api_key is None:
            return None
        return self.api_key.get_secret_value()


@llm_provider("openai", None)
class OpenAIWrapper(LLMWrapper):
    __used_options__: ClassVar = [OpenAIKey]

    def __init__(self, model: str, options: Options):
        import openai

        self.model = model
        self.client = openai.OpenAI(api_key=options.get(OpenAIKey).get_value())

    def complete(self, messages: List[LLMMessage]) -> str:
        import openai

        messages = [{"role": user, "content": msg} for user, msg in messages]
        try:
            response = self.client.chat.completions.create(model=self.model, messages=messages)  # type: ignore[arg-type]
        except openai.OpenAIError as e:
            raise LLMRequestError("Failed to call OpenAI complete API") from e
        content = response.choices[0].message.content
        assert content is not None  # todo: better error
        return content


@llm_provider("litellm", None)
class LiteLLMWrapper(LLMWrapper):
    def __init__(self, model: str):
        self.model = model

    def complete(self, messages: List[LLMMessage]) -> str:
        from litellm import completion

        return completion(model=self.model, messages=messages).choices[0].message.content
