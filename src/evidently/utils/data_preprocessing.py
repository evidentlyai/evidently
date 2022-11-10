from enum import Enum
from typing import List, Optional, Union

import dataclasses


class ColumnType(Enum):
    Categorical = "cat"
    Numerical = "num"
    Datetime = "datetime"


@dataclasses.dataclass
class ColumnDefinition:
    column_name: str
    column_type: ColumnType


@dataclasses.dataclass
class PredictionColumns:
    predicted_values: Optional[ColumnDefinition]
    prediction_probas: List[ColumnDefinition]


def _check_filter(column: ColumnDefinition, filter_def: str) -> bool:
    if filter_def == "all":
        return True
    if filter_def == "categorical_column":
        return column.column_type == ColumnType.Categorical
    if filter_def == "numerical_column":
        return column.column_type == ColumnType.Numerical
    if filter_def == "datetime_column":
        return column.column_type == ColumnType.Datetime
    raise ValueError(f"Unknown filter: {filter_def}")


@dataclasses.dataclass
class DataDefinition:
    _columns: List[ColumnDefinition]
    _target: Optional[ColumnDefinition]
    _prediction_columns: Optional[PredictionColumns]
    _task: str
    _classification_labels: List[Union[int, str]]

    def __init__(
            self,
            columns: List[ColumnDefinition],
            target: Optional[ColumnDefinition],
            prediction_columns: Optional[PredictionColumns],
            task: str,
            classification_labels: List[Union[int, str]]):
        self._columns = columns
        self._task = task
        self._target = target
        self._prediction_columns = prediction_columns
        self._classification_labels = classification_labels

    def get_columns(self, filter_def: str = "all") -> List[ColumnDefinition]:
        return [column for column in self._columns if _check_filter(column, filter_def)]

    def get_target_column(self) -> Optional[ColumnDefinition]:
        return self._target

    def get_prediction_columns(self) -> Optional[PredictionColumns]:
        return self._prediction_columns

    def task(self) -> str:
        return self._task

    def classification_labels(self) -> List[Union[int, str]]:
        return self._classification_labels
