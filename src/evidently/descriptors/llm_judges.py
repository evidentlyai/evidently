from typing import Any
from typing import Dict
from typing import Iterator
from typing import List
from typing import Optional
from typing import Union

import pandas as pd

from evidently import ColumnType
from evidently import Dataset
from evidently._pydantic_compat import PrivateAttr
from evidently.core.datasets import AnyDescriptorTest
from evidently.core.datasets import DatasetColumn
from evidently.core.datasets import Descriptor
from evidently.legacy.base_metric import DisplayName
from evidently.legacy.options.base import Options
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.utils.data_preprocessing import create_data_definition
from evidently.legacy.utils.llm.wrapper import LLMMessage as LegacyLLMMessage
from evidently.legacy.utils.llm.wrapper import LLMRequest
from evidently.legacy.utils.llm.wrapper import LLMWrapper
from evidently.legacy.utils.llm.wrapper import get_llm_wrapper
from evidently.llm.models import LLMMessage
from evidently.llm.prompts.content import MessagesPromptContent
from evidently.llm.prompts.content import PromptContent
from evidently.llm.prompts.content import TemplatePromptContent
from evidently.llm.templates import *  # noqa: F403
from evidently.llm.templates import BaseLLMPromptTemplate


class GenericLLMDescriptor(Descriptor):
    input_columns: Dict[str, str]
    provider: str
    model: str
    prompt: PromptContent

    _llm_wrapper: Optional[LLMWrapper] = PrivateAttr(None)

    def __init__(
        self,
        provider: str,
        model: str,
        input_columns: Dict[str, str],
        prompt: Union[List[LLMMessage], PromptContent],
        alias: str,
        tests: Optional[List[AnyDescriptorTest]] = None,
        **data: Any,
    ):
        self.prompt = MessagesPromptContent(messages=prompt) if isinstance(prompt, list) else prompt
        self.input_columns = input_columns
        self.model = model
        self.provider = provider
        super().__init__(alias, tests, **data)

    def get_llm_wrapper(self, options: Options) -> LLMWrapper:
        if self._llm_wrapper is None:
            self._llm_wrapper = get_llm_wrapper(self.provider, self.model, options)
        return self._llm_wrapper

    def _fmt_messages(self, values: Dict[str, Any]) -> List[LegacyLLMMessage]:
        return [LegacyLLMMessage(role=m.role, content=m.content.format(**values)) for m in self.prompt.as_messages()]

    def iterate_messages(self, dataset: Dataset) -> Iterator[LLMRequest[str]]:
        for _, column_values in (
            dataset.as_dataframe()[list(self.input_columns)].rename(columns=self.input_columns).iterrows()
        ):
            yield LLMRequest(
                messages=self._fmt_messages(column_values.to_dict()),
                response_parser=self.prompt.get_parser(),
                response_type=self.prompt.get_response_type(),
            )

    def generate_data(
        self, dataset: "Dataset", options: Options
    ) -> Union[DatasetColumn, Dict[DisplayName, DatasetColumn]]:
        result = self.get_llm_wrapper(options).run_batch_sync(requests=self.iterate_messages(dataset))
        if isinstance(result, list) and any(isinstance(o, dict) for o in result):
            df = pd.DataFrame(result)

            if isinstance(self.prompt, TemplatePromptContent):
                columns = [
                    (col, self.prompt.template.get_type(col)) for col in self.prompt.template.list_output_columns()
                ]
            else:
                columns = [(col, ColumnType.Text) for col in df.columns]

            return {
                f"{self.alias} {col}": DatasetColumn(
                    col_type,
                    df[col].astype(float) if col_type == ColumnType.Numerical else df[col],
                )
                for (col, col_type) in columns
            }
        if isinstance(self.prompt, TemplatePromptContent):
            column_type = self.prompt.template.get_type(self.prompt.template.get_main_output_column())
            if column_type == ColumnType.Numerical:
                column_data = pd.Series(result).astype(float)
            else:
                column_data = pd.Series(result)
            return DatasetColumn(
                column_type,
                column_data,
            )
        return DatasetColumn(ColumnType.Text, pd.Series(result))


class LLMEval(Descriptor):
    provider: str
    model: str
    input_column: Optional[str] = None
    input_columns: Optional[Dict[str, str]] = None
    template: BaseLLMPromptTemplate

    # _llm_wrapper: Optional[LLMWrapper] = PrivateAttr(None)
    @property
    def _judge(self):
        from evidently.legacy.features.llm_judge import LLMJudge

        return LLMJudge(
            display_name=self.alias,
            provider=self.provider,
            model=self.model,
            input_column=self.input_column,
            input_columns=self.input_columns,
            template=self.template,
        )

    def get_dataset_column(self, column_name: str, values: pd.Series) -> DatasetColumn:
        column_type = self._judge.get_type(column_name)
        if column_type == ColumnType.Numerical:
            values = pd.to_numeric(values, errors="coerce")
        dataset_column = DatasetColumn(type=column_type, data=values)
        return dataset_column

    def generate_data(
        self, dataset: "Dataset", options: Options
    ) -> Union[DatasetColumn, Dict[DisplayName, DatasetColumn]]:
        judge = self._judge
        feature = judge.generate_features_renamed(
            dataset.as_dataframe(),
            create_data_definition(None, dataset.as_dataframe(), ColumnMapping()),
            options,
        )
        return {col.display_name: self.get_dataset_column(col.name, feature[col.name]) for col in judge.list_columns()}

    def list_output_columns(self) -> List[str]:
        return [c.display_name for c in self._judge.list_columns()]
