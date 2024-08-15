import json
from abc import ABC
from abc import abstractmethod
from enum import Enum
from typing import Callable
from typing import Dict
from typing import Iterator
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import pandas as pd

from evidently import ColumnType
from evidently._pydantic_compat import Field
from evidently._pydantic_compat import PrivateAttr
from evidently.base_metric import ColumnName
from evidently.features.generated_features import GeneratedFeatures
from evidently.pydantic_utils import EnumValueMixin
from evidently.pydantic_utils import EvidentlyBaseModel
from evidently.utils.data_preprocessing import DataDefinition

LLMMessage = Tuple[str, str]
LLMResponse = Dict[str, Union[str, float]]


class LLMResponseParseError(ValueError):
    pass


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


class BaseLLMPromptTemplate(EvidentlyBaseModel, ABC):
    @abstractmethod
    def iterate_messages(self, data: pd.DataFrame, input_columns: Dict[str, str]) -> Iterator[LLMMessage]:
        raise NotImplementedError

    @abstractmethod
    def get_system_prompts(self) -> List[LLMMessage]:
        raise NotImplementedError

    @abstractmethod
    def parse_response(self, response: str) -> LLMResponse:
        raise NotImplementedError

    @abstractmethod
    def list_output_columns(self) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def get_type(self, subcolumn: Optional[str]) -> ColumnType:
        raise NotImplementedError

    @abstractmethod
    def get_prompt_template(self) -> str:
        raise NotImplementedError


class Uncertainty(str, Enum):
    UNKNOWN = "unknown"
    TARGET = "target"
    NON_TARGET = "non_target"


class BinaryClassificationPromptTemplate(BaseLLMPromptTemplate, EnumValueMixin):
    template: str = (
        """{__criteria__}\n{__task__}\n\n{__as__}\n{{input}}\n{__ae__}\n\n{__instructions__}\n\n{__output_format__}"""
    )
    criteria: str = ""
    instructions_template: str = (
        "Use the following categories for classification:\n{__categories__}\n{__scoring__}\nThink step by step."
    )
    anchor_start: str = "___text_starts_here___"
    anchor_end: str = "___text_ends_here___"

    placeholders: Dict[str, str] = {}
    target_category: str
    non_target_category: str

    uncertainty: Uncertainty = Uncertainty.UNKNOWN

    include_category: bool = True
    include_reasoning: bool = False
    include_score: bool = False
    score_range: Tuple[float, float] = (0.0, 1.0)

    output_column: str = "category"
    output_reasoning_column: str = "reasoning"
    output_score_column: str = "score"

    pre_messages: List[LLMMessage] = Field(default_factory=list)

    def iterate_messages(self, data: pd.DataFrame, input_columns: Dict[str, str]) -> Iterator[LLMMessage]:
        prompt_template = self.get_prompt_template()
        for _, column_values in data[list(input_columns)].rename(columns=input_columns).iterrows():
            yield "user", prompt_template.format(**dict(column_values))

    def get_prompt_template(self) -> str:
        values = {
            "__criteria__": self._criteria(),
            "__task__": self._task(),
            "__instructions__": self._instructions(),
            "__output_format__": self._output_format(),
            "__as__": self.anchor_start,
            "__ae__": self.anchor_end,
            **self.placeholders,
        }
        return self.template.format(**values)

    def _task(self):
        return (
            f"Classify text between {self.anchor_start} and {self.anchor_end} "
            f"into two categories: {self.target_category} and {self.non_target_category}."
        )

    def _criteria(self):
        return self.criteria

    def _instructions(self):
        categories = (
            (
                f"{self.target_category}: if text is {self.target_category.lower()}\n"
                + f"{self.non_target_category}: if text is {self.non_target_category.lower()}\n"
                + f"{self._uncertainty_class()}: use this category only if the information provided "
                f"is not sufficient to make a clear determination\n"
            )
            if self.include_category
            else ""
        )
        lower, upper = self.score_range
        scoring = (
            (
                f"Score text in range from {lower} to {upper} "
                f"where {lower} is absolute {self.non_target_category} and {upper} is absolute {self.target_category}"
            )
            if self.include_score
            else ""
        )
        return self.instructions_template.format(__categories__=categories, __scoring__=scoring)

    def _uncertainty_class(self):
        if self.uncertainty is Uncertainty.UNKNOWN:
            return "UNKNOWN"
        if self.uncertainty is Uncertainty.NON_TARGET:
            return self.non_target_category
        if self.uncertainty is Uncertainty.TARGET:
            return self.target_category
        raise ValueError(f"Unknown uncertainty value: {self.uncertainty}")

    def _output_format(self):
        values = []
        columns = {}
        if self.include_category:
            cat = f"{self.target_category} or {self.non_target_category}"
            if self.uncertainty == Uncertainty.UNKNOWN:
                cat += " or UNKNOWN"
            columns[self.output_column] = f'"{cat}"'
            values.append("category")
        if self.include_score:
            columns[self.output_score_column] = "<score here>"
            values.append("score")
        if self.include_reasoning:
            columns[self.output_reasoning_column] = '"<reasoning here>"'
            values.append("reasoning")

        keys = "\n".join(f'"{k}": {v}' for k, v in columns.items())
        return f"Return {', '.join(values)} formatted as json without formatting as follows:\n{{{{\n{keys}\n}}}}"

    def parse_response(self, response: str) -> LLMResponse:
        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            raise LLMResponseParseError(f"Failed to parse response '{response}' as json") from e

    def list_output_columns(self) -> List[str]:
        result = []
        if self.include_category:
            result.append(self.output_column)
        if self.include_score:
            result.append(self.output_score_column)
        if self.include_reasoning:
            result.append(self.output_reasoning_column)
        return result

    def get_type(self, subcolumn: Optional[str]) -> ColumnType:
        if subcolumn == self.output_reasoning_column:
            return ColumnType.Text
        if subcolumn == self.output_score_column:
            return ColumnType.Numerical
        if subcolumn == self.output_column:
            return ColumnType.Categorical
        raise ValueError(f"Unknown subcolumn {subcolumn}")

    def get_system_prompts(self) -> List[LLMMessage]:
        return self.pre_messages


class LLMJudge(GeneratedFeatures):
    """Generic LLM judge generated features"""

    provider: str
    model: str

    input_column: Optional[str] = None
    input_columns: Optional[Dict[str, str]] = None
    template: BaseLLMPromptTemplate

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
        result: List[Dict[str, Union[str, float]]] = []

        for message in self.template.iterate_messages(data, self.get_input_columns()):
            messages: List[LLMMessage] = [*self.template.get_system_prompts(), message]
            response = self.llm_wrapper.complete(messages)
            result.append(self.template.parse_response(response))
        return pd.DataFrame(result)

    def list_columns(self) -> List["ColumnName"]:
        return [
            self._create_column(c, display_name=f"{self.display_name or ''} {c}")
            for c in self.template.list_output_columns()
        ]

    def get_type(self, subcolumn: Optional[str] = None) -> ColumnType:
        if subcolumn is not None:
            subcolumn = self._extract_subcolumn_name(subcolumn)

        return self.template.get_type(subcolumn)


@llm_provider("openai", None)
class OpenAIWrapper(LLMWrapper):
    def __init__(self, model: str):
        import openai

        self.model = model
        self.client = openai.OpenAI()

    def complete(self, messages: List[LLMMessage]) -> str:
        messages = [{"role": user, "content": msg} for user, msg in messages]
        response = self.client.chat.completions.create(model="gpt-4o-mini", messages=messages)  # type: ignore[arg-type]
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
