import abc
import logging
from dataclasses import dataclass
from enum import Enum
from typing import Generic
from typing import List
from typing import Optional
from typing import TypeVar
from typing import Union

import pandas as pd

from evidently.features.generated_features import GeneratedFeature
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.utils.data_preprocessing import DataDefinition

TResult = TypeVar("TResult")


class ErrorResult:
    exception: BaseException

    def __init__(self, exception: BaseException):
        self.exception = exception


class DatasetType(Enum):
    MAIN = "main"
    ADDITIONAL = "additional"


@dataclass(eq=True, unsafe_hash=True)
class ColumnName:
    name: str
    dataset: DatasetType
    feature_class: Optional[GeneratedFeature]


def additional_feature(feature: GeneratedFeature, feature_name: str) -> ColumnName:
    return ColumnName(
        name=feature.__class__.__name__ + "." + feature_name,
        dataset=DatasetType.ADDITIONAL,
        feature_class=feature,
    )


@dataclass
class InputData:
    reference_data: Optional[pd.DataFrame]
    current_data: pd.DataFrame
    reference_additional_features: Optional[pd.DataFrame]
    current_additional_features: Optional[pd.DataFrame]
    column_mapping: ColumnMapping
    data_definition: DataDefinition

    @staticmethod
    def _get_by_column_name(dataset: pd.DataFrame, additional: pd.DataFrame, column: ColumnName) -> pd.Series:
        if column.dataset == DatasetType.MAIN:
            return dataset[column.name]
        if column.dataset == DatasetType.ADDITIONAL:
            return additional[column.name]
        raise ValueError("unknown column data")

    def get_current_column(self, column: Union[str, ColumnName]) -> pd.Series:
        if isinstance(column, str):
            _column = ColumnName(column, DatasetType.MAIN, None)
        else:
            _column = column
        return self._get_by_column_name(self.current_data, self.current_additional_features, _column)

    def get_reference_column(self, column: Union[str, ColumnName]) -> Optional[pd.Series]:
        if self.reference_data is None:
            return None
        if isinstance(column, str):
            _column = ColumnName(column, DatasetType.MAIN, None)
        else:
            _column = column
        if self.reference_additional_features is None and _column.dataset == DatasetType.ADDITIONAL:
            return None
        return self._get_by_column_name(self.reference_data, self.reference_additional_features, _column)


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

    def get_parameters(self) -> Optional[tuple]:
        attributes = []
        for field, value in sorted(self.__dict__.items(), key=lambda x: x[0]):
            if field in ["context"]:
                continue
            if isinstance(value, list):
                attributes.append(tuple(value))
            else:
                attributes.append(value)
        params = tuple(attributes)
        try:
            hash(params)
        except TypeError:
            logging.warning(f"unhashable params for {type(self)}. Fallback to unique.")
            return None
        return params

    def required_features(self, data_definition: DataDefinition) -> List[GeneratedFeature]:
        required_features = []
        for field, value in sorted(self.__dict__.items(), key=lambda x: x[0]):
            if field in ["context"]:
                continue
            if issubclass(type(value), ColumnName) and value.feature_class is not None:
                required_features.append(value.feature_class)
        return required_features
