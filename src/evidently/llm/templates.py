from abc import abstractmethod
from enum import Enum
from typing import Dict
from typing import Iterator
from typing import List
from typing import Literal
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Union

import pandas as pd

from evidently._pydantic_compat import Field
from evidently.core.datasets import ColumnType
from evidently.llm.models import LLMMessage
from evidently.llm.utils.blocks import PromptBlock
from evidently.llm.utils.templates import BlockPromptTemplate
from evidently.llm.utils.wrapper import LLMRequest
from evidently.pydantic_utils import EnumValueMixin


class BaseLLMPromptTemplate(BlockPromptTemplate):
    class Config:
        is_base_type = True

    def iterate_messages(self, data: pd.DataFrame, input_columns: Dict[str, str]) -> Iterator[LLMRequest[dict]]:
        for _, column_values in data[list(input_columns)].rename(columns=input_columns).iterrows():
            yield LLMRequest(
                messages=self.get_messages(column_values), response_parser=self.get_parser(), response_type=dict
            )

    @abstractmethod
    def list_output_columns(self) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def get_type(self, subcolumn: Optional[str]) -> ColumnType:
        raise NotImplementedError

    @abstractmethod
    def get_main_output_column(self) -> str:
        raise NotImplementedError


class Uncertainty(str, Enum):
    UNKNOWN = "unknown"
    TARGET = "target"
    NON_TARGET = "non_target"


class BinaryClassificationPromptTemplate(BaseLLMPromptTemplate, EnumValueMixin):
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

    def get_blocks(self) -> Sequence[PromptBlock]:
        fields = {}
        if self.include_category:
            cat = f"{self.target_category} or {self.non_target_category}"
            if self.uncertainty == Uncertainty.UNKNOWN:
                cat += " or UNKNOWN"
            fields["category"] = (cat, self.output_column)
        if self.include_score:
            fields["score"] = ("<score here>", self.output_score_column)
        if self.include_reasoning:
            fields["reasoning"] = ("<reasoning here>", self.output_reasoning_column)
        return [
            PromptBlock.simple(self.criteria),
            PromptBlock.simple(
                f"Classify text between {self.anchor_start} and {self.anchor_end} "
                f"into two categories: {self.target_category} and {self.non_target_category}."
            ),
            PromptBlock.input().anchored(self.anchor_start, self.anchor_end),
            PromptBlock.simple(self._instructions()),
            PromptBlock.json_output(**fields),
        ]

    def get_messages(self, values) -> List[LLMMessage]:
        return [*self.pre_messages, *super().get_messages(values)]

    def list_output_columns(self) -> List[str]:
        result = []
        if self.include_category:
            result.append(self.output_column)
        if self.include_score:
            result.append(self.output_score_column)
        if self.include_reasoning:
            result.append(self.output_reasoning_column)
        return result

    def get_main_output_column(self) -> str:
        return self.output_column

    def get_type(self, subcolumn: Optional[str]) -> ColumnType:
        if subcolumn == self.output_reasoning_column:
            return ColumnType.Text
        if subcolumn == self.output_score_column:
            return ColumnType.Numerical
        if subcolumn == self.output_column or subcolumn is None:
            return ColumnType.Categorical
        raise ValueError(f"Unknown subcolumn {subcolumn}")


class MulticlassClassificationPromptTemplate(BaseLLMPromptTemplate, EnumValueMixin):
    criteria: str = ""
    instructions_template: str = (
        "Use the following categories for classification:\n{__categories__}\n{__scoring__}\nThink step by step."
    )

    anchor_start: str = "___text_starts_here___"
    anchor_end: str = "___text_ends_here___"
    uncertainty: Union[Literal["UNKNOWN"], str] = "UNKNOWN"

    category_criteria: Dict[str, str] = {}

    include_category: bool = True
    include_reasoning: bool = False
    include_score: bool = False
    score_range: Tuple[float, float] = (0.0, 1.0)

    output_column: str = "category"
    output_reasoning_column: str = "reasoning"
    output_score_column_prefix: str = "score"

    pre_messages: List[LLMMessage] = Field(default_factory=list)

    def get_blocks(self) -> Sequence[PromptBlock]:
        fields: Dict[str, Tuple[str, str]] = {}
        if self.include_category:
            cat = " or ".join(self.category_criteria.keys())
            if self.uncertainty == Uncertainty.UNKNOWN:
                cat += " or UNKNOWN"
            fields["category"] = (cat, self.output_column)
        if self.include_score:
            fields.update(
                {
                    f"score_{cat}": (f"<score for {cat} here>", self.get_score_column(cat))
                    for cat in self.category_criteria.keys()
                }
            )
        if self.include_reasoning:
            fields["reasoning"] = ("<reasoning here>", self.output_reasoning_column)
        return [
            PromptBlock.simple(self.criteria),
            PromptBlock.simple(
                f"Classify text between {self.anchor_start} and {self.anchor_end} "
                f"into categories: " + " or ".join(self.category_criteria.keys()) + "."
            ),
            PromptBlock.input().anchored(self.anchor_start, self.anchor_end),
            PromptBlock.simple(self._instructions()),
            PromptBlock.json_output(**fields),
        ]

    def get_score_column(self, category: str) -> str:
        return f"{self.output_score_column_prefix}_{category}"

    def list_output_columns(self) -> List[str]:
        result = []
        if self.include_category:
            result.append(self.output_column)
        if self.include_score:
            result.extend(self.get_score_column(cat) for cat in self.category_criteria.keys())
        if self.include_reasoning:
            result.append(self.output_reasoning_column)
        return result

    def get_main_output_column(self) -> str:
        return self.output_column

    def get_type(self, subcolumn: Optional[str]) -> ColumnType:
        if subcolumn == self.output_reasoning_column:
            return ColumnType.Text
        if subcolumn == self.output_column or subcolumn is None:
            return ColumnType.Categorical
        if subcolumn.startswith(self.output_score_column_prefix):
            return ColumnType.Numerical
        raise ValueError(f"Unknown subcolumn {subcolumn}")

    def _instructions(self):
        categories = (
            (
                "\n".join(f"{cat}: {crit}" for cat, crit in self.category_criteria.items())
                + "\n"
                + f"{self._uncertainty_class()}: use this category only if the information provided "
                f"is not sufficient to make a clear determination\n"
            )
            if self.include_category
            else ""
        )
        lower, upper = self.score_range
        scoring = (f"For each category, score text in range from {lower} to {upper}") if self.include_score else ""
        return self.instructions_template.format(__categories__=categories, __scoring__=scoring)

    def _uncertainty_class(self):
        if self.uncertainty.upper() == "UNKNOWN":
            return "UNKNOWN"
        if self.uncertainty not in self.category_criteria:
            raise ValueError(f"Unknown uncertainty value: {self.uncertainty}")
        return self.uncertainty

    def get_messages(self, values) -> List[LLMMessage]:
        return [*self.pre_messages, *super().get_messages(values)]
