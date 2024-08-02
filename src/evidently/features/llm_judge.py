import json
import os
from abc import ABC
from abc import abstractmethod
from typing import Callable
from typing import Dict
from typing import Iterator
from typing import List
from typing import Optional
from typing import Tuple

import pandas as pd

from evidently._pydantic_compat import Field
from evidently._pydantic_compat import PrivateAttr
from evidently.base_metric import ColumnName
from evidently.features.generated_features import GeneratedFeatures
from evidently.pydantic_utils import EvidentlyBaseModel
from evidently.utils.data_preprocessing import DataDefinition

LLMMessage = Tuple[str, str]


class LLMWrapper(ABC):
    @abstractmethod
    def complete(self, messages: List[LLMMessage]) -> str:
        raise NotImplementedError


LLMProvider = str
LLMModel = str
LLMWrapperProvider = Callable[[LLMModel], LLMWrapper]
_wrappers: Dict[Tuple[LLMProvider, Optional[LLMModel]], LLMWrapperProvider] = {}


def llm_provider(name: LLMProvider, model: Optional[LLMModel]):
    def dec(f: LLMWrapperProvider):
        _wrappers[(name, model)] = f
        return f

    return dec


def get_llm_wrapper(provider: LLMProvider, model: LLMModel) -> LLMWrapper:
    key: Tuple[str, Optional[str]] = (provider, model)
    if key in _wrappers:
        return _wrappers[key](model)
    key = (provider, None)
    if key in _wrappers:
        return _wrappers[key](model)
    raise ValueError(f"LLM wrapper for provider {provider} model {model} not found")


class LLMPromtTemplate(EvidentlyBaseModel):
    template: str = """{__task__}\n\n{{input}}\n\n{__instructions__}\n\n{__output_format__}"""
    task: str
    instructions_template: str

    placeholders: Dict[str, str] = {}
    categories: Optional[Dict[str, str]] = None

    include_reasoning: bool = False
    return_json: bool = True
    output_column: str = "result"
    output_reasoning_column: str = "reasoning"

    def iterate_messages(self, data: pd.DataFrame, input_columns: Dict[str, str]) -> Iterator[Tuple[str, str]]:
        promt_template = self._promt_template()
        for _, column_values in data[list(input_columns)].rename(columns=input_columns).iterrows():
            yield "user", promt_template.format(**dict(column_values))

    def _promt_template(self) -> str:
        values = {
            "__task__": self._task(),
            "__instructions__": self._instructions(),
            "__output_format__": self._output_format(),
            **self.placeholders,
        }
        return self.template.format(**values)

    def _task(self):
        return self.task

    def _instructions(self):
        categories = "\n".join(f"{cat}: if {condition}" for cat, condition in self.categories.items())
        return self.instructions_template.format(categories=categories)

    def _output_format(self):
        output_format = "Return category only" if not self.include_reasoning else "Return category and reasoning"
        if self.return_json:
            output_format = (
                output_format
                + f' formatted as json string without formatting with key "{self.output_column}" for category'
            )
            if self.include_reasoning:
                output_format = output_format + f' and key "{self.output_reasoning_column}" for reasoning'
        return output_format

    def parse_response(self, response: str) -> Dict[str, str]:
        if self.return_json:
            return json.loads(response)
        assert self.categories is not None  # todo: should it be optional?
        result = next(category for category in self.categories if category in response)
        if self.include_reasoning:
            return {self.output_column: result, self.output_reasoning_column: response}
        return {self.output_column: result}

    def list_output_columns(self) -> List[str]:
        result = [self.output_column]
        if self.include_reasoning:
            result.append(self.output_reasoning_column)
        return result


class LLMJudge(GeneratedFeatures):
    """Generic LLM judge generated features"""

    provider: str
    model: str

    input_column: Optional[str] = None
    input_columns: Optional[Dict[str, str]] = None
    template: LLMPromtTemplate

    pre_messages: Tuple[LLMMessage] = Field(default_factory=tuple)

    _llm_wrapper: Optional[LLMWrapper] = PrivateAttr(None)

    @property
    def llm_wrapper(self) -> LLMWrapper:
        if self._llm_wrapper is None:
            self._llm_wrapper = get_llm_wrapper(self.provider, self.model)
        return self._llm_wrapper

    def get_input_columns(self):
        if self.input_column is None:
            assert self.input_columns is not None  # todo: validate earlier
            return self.input_columns

        return {self.input_column: "input"}

    def generate_features(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.DataFrame:
        result: List[Dict[str, str]] = []

        for message in self.template.iterate_messages(data, self.get_input_columns()):
            messages: List[LLMMessage] = [*self.pre_messages, message]
            response = self.llm_wrapper.complete(messages)
            result.append(self.template.parse_response(response))
        return pd.DataFrame(result)

    def list_columns(self) -> List["ColumnName"]:
        return [self._create_column(c) for c in self.template.list_output_columns()]


@llm_provider("openai", None)
class OpenAIWrapper(LLMWrapper):
    def __init__(self, model: str):
        import openai

        self.model = model
        openai_api_key = os.environ.get("OPEN_AI_API_KEY")  # todo: better creds
        self.client = openai.OpenAI(api_key=openai_api_key)

    def complete(self, messages: List[LLMMessage]) -> str:
        messages = [{"role": user, "content": msg} for user, msg in messages]
        response = self.client.chat.completions.create(model="gpt-4o-mini", messages=messages)  # type: ignore[arg-type]
        content = response.choices[0].message.content
        assert content is not None  # todo: better error
        return content
