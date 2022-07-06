import abc
from dataclasses import dataclass
from typing import Generic
from typing import Tuple
from typing import TypeVar
from typing import Optional

import pandas as pd

from evidently.pipeline.column_mapping import ColumnMapping

TResult = TypeVar("TResult")


@dataclass
class InputData:
    reference_data: Optional[pd.DataFrame]
    current_data: pd.DataFrame
    column_mapping: ColumnMapping


class Metric(Generic[TResult]):
    context = None

    @abc.abstractmethod
    def calculate(self, data: InputData, metrics: dict) -> TResult:
        raise NotImplementedError()

    def set_context(self, context):
        self.context = context

    def get_result(self) -> TResult:
        if self.context is None:
            raise ValueError("No context is set")
        result = self.context.metric_results.get(self, None)
        if result is None:
            raise ValueError(f"No result found for metric {self} of type {type(self).__name__}")
        return result
