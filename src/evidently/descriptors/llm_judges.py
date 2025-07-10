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
from evidently.legacy.utils.llm.wrapper import LLMMessage as LegacyLLMMessage
from evidently.legacy.utils.llm.wrapper import LLMRequest
from evidently.legacy.utils.llm.wrapper import LLMWrapper
from evidently.legacy.utils.llm.wrapper import get_llm_wrapper
from evidently.llm.models import LLMMessage
from evidently.llm.prompts.content import MessagesPromptContent
from evidently.llm.prompts.content import PromptContent
from evidently.llm.templates import *  # noqa: F403


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
                messages=self._fmt_messages(column_values.to_dict()), response_parser=lambda x: x, response_type=str
            )

    def generate_data(
        self, dataset: "Dataset", options: Options
    ) -> Union[DatasetColumn, Dict[DisplayName, DatasetColumn]]:
        result = self.get_llm_wrapper(options).run_batch_sync(requests=self.iterate_messages(dataset))

        return DatasetColumn(ColumnType.Text, pd.Series(result))
