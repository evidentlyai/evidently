import abc
from dataclasses import dataclass
from typing import Generic
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

    def get_id(self) -> str:
        return self.__class__.__name__

    @abc.abstractmethod
    def calculate(self, data: InputData) -> TResult:
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

    def get_parameters(self) -> tuple:
        attributes = []
        for field, value in sorted(self.__dict__.items(), key=lambda x: x[0]):
            if field in ["context"]:
                continue
            if isinstance(value, list):
                attributes.append(tuple(value))
            else:
                attributes.append(value)
        return tuple(attributes)
