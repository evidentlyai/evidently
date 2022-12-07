import abc
from typing import Dict
from typing import Generic
from typing import Optional
from typing import Type
from typing import TypeVar
from typing import Union

import pandas as pd
from dataclasses import dataclass

from evidently.pipeline.column_mapping import ColumnMapping
from evidently.utils.data_preprocessing import DataDefinition
from evidently.utils.generators import BaseGenerator
from evidently.utils.generators import make_generator_by_columns

TResult = TypeVar("TResult")


class ErrorResult:
    exception: BaseException

    def __init__(self, exception: BaseException):
        self.exception = exception


@dataclass
class InputData:
    reference_data: Optional[pd.DataFrame]
    current_data: pd.DataFrame
    column_mapping: ColumnMapping
    data_definition: DataDefinition


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
        if isinstance(result, ErrorResult):
            raise result.exception
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


def generate_column_metrics(
    metric_class: Type[Metric],
    columns: Optional[Union[str, list]] = None,
    parameters: Optional[Dict] = None,
    skip_id_column: bool = False,
) -> BaseGenerator:
    """Function for generating metrics for columns"""
    return make_generator_by_columns(
        base_class=metric_class,
        columns=columns,
        parameters=parameters,
        skip_id_column=skip_id_column,
    )
