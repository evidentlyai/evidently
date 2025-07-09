from typing import ClassVar
from typing import Dict
from typing import List
from typing import Optional

import pandas as pd

from evidently._pydantic_compat import PrivateAttr
from evidently.legacy.base_metric import ColumnName
from evidently.legacy.core import ColumnType
from evidently.legacy.features.generated_features import GeneratedFeatures
from evidently.legacy.options.base import Options
from evidently.legacy.utils.data_preprocessing import DataDefinition
from evidently.llm.models import LLMMessage
from evidently.llm.templates import BaseLLMPromptTemplate
from evidently.llm.templates import BinaryClassificationPromptTemplate
from evidently.llm.templates import MulticlassClassificationPromptTemplate
from evidently.llm.templates import Uncertainty
from evidently.llm.utils.wrapper import LLMWrapper
from evidently.llm.utils.wrapper import get_llm_wrapper


class LLMJudge(GeneratedFeatures):
    class Config:
        type_alias = "evidently:feature:LLMJudge"

    """Generic LLM judge generated features"""

    DEFAULT_INPUT_COLUMN: ClassVar = "input"

    provider: str
    model: str

    input_column: Optional[str] = None
    input_columns: Optional[Dict[str, str]] = None
    template: BaseLLMPromptTemplate

    _llm_wrapper: Optional[LLMWrapper] = PrivateAttr(None)

    def get_llm_wrapper(self, options: Options) -> LLMWrapper:
        if self._llm_wrapper is None:
            self._llm_wrapper = get_llm_wrapper(self.provider, self.model, options)
        return self._llm_wrapper

    def get_input_columns(self):
        if self.input_column is None:
            assert self.input_columns is not None  # todo: validate earlier
            return self.input_columns

        return {self.input_column: self.DEFAULT_INPUT_COLUMN}

    def generate_features(self, data: pd.DataFrame, data_definition: DataDefinition, options: Options) -> pd.DataFrame:
        result = self.get_llm_wrapper(options).run_batch_sync(
            requests=self.template.iterate_messages(data, self.get_input_columns())
        )

        return pd.DataFrame(result)

    def list_columns(self) -> List["ColumnName"]:
        main_col = self.template.get_main_output_column()
        return [
            self._create_column(c, display_name=f"{self.display_name or ''} {c if c != main_col else ''}".strip())
            for c in self.template.list_output_columns()
        ]

    def get_type(self, subcolumn: Optional[str] = None) -> ColumnType:
        if subcolumn is not None:
            subcolumn = self._extract_subcolumn_name(subcolumn)

        return self.template.get_type(subcolumn)


__all__ = [
    "LLMJudge",
    "BinaryClassificationPromptTemplate",
    "MulticlassClassificationPromptTemplate",
    "BaseLLMPromptTemplate",
    "Uncertainty",
    "LLMMessage",
    "LLMWrapper",
]
