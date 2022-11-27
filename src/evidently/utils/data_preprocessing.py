from enum import Enum
from typing import List
from typing import Optional
from typing import Sequence
from typing import Union

import dataclasses
import numpy as np
import pandas as pd

from evidently import ColumnMapping
from evidently import TaskType


@dataclasses.dataclass
class _InputData:
    reference: Optional[pd.DataFrame]
    current: pd.DataFrame


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
    predicted_values: Optional[ColumnDefinition] = None
    prediction_probas: Optional[List[ColumnDefinition]] = None

    def get_columns_list(self) -> List[ColumnDefinition]:
        result = [self.predicted_values]
        if self.prediction_probas is not None:
            result.extend(self.prediction_probas)
        return [col for col in result if col is not None]


def _check_filter(column: ColumnDefinition, utility_columns: List[str], filter_def: str) -> bool:
    if filter_def == "all":
        return True
    if filter_def == "categorical_columns":
        return column.column_type == ColumnType.Categorical
    if filter_def == "numerical_columns":
        return column.column_type == ColumnType.Numerical
    if filter_def == "datetime_columns":
        return column.column_type == ColumnType.Datetime
    if filter_def == "all_features":
        return column.column_name not in utility_columns
    if filter_def == "categorical_features":
        return column.column_type == ColumnType.Categorical and column.column_name not in utility_columns
    if filter_def == "numerical_features":
        return column.column_type == ColumnType.Numerical and column.column_name not in utility_columns
    if filter_def == "datetime_features":
        return column.column_type == ColumnType.Datetime and column.column_name not in utility_columns
    raise ValueError(f"Unknown filter: {filter_def}")


@dataclasses.dataclass
class DataDefinition:
    _columns: List[ColumnDefinition]
    _target: Optional[ColumnDefinition]
    _prediction_columns: Optional[PredictionColumns]
    _id_column: Optional[ColumnDefinition]
    _datetime_column: Optional[ColumnDefinition]

    _task: Optional[str]
    _classification_labels: Optional[Sequence[str]]

    def __init__(
        self,
        columns: List[ColumnDefinition],
        target: Optional[ColumnDefinition],
        prediction_columns: Optional[PredictionColumns],
        id_column: Optional[ColumnDefinition],
        datetime_column: Optional[ColumnDefinition],
        task: Optional[str],
        classification_labels: Optional[Sequence[str]],
    ):
        self._columns = columns
        self._id_column = id_column
        self._datetime_column = datetime_column
        self._task = task
        self._target = target
        self._prediction_columns = prediction_columns
        self._classification_labels = classification_labels

    def get_columns(self, filter_def: str = "all") -> List[ColumnDefinition]:
        if self._prediction_columns is not None:
            prediction = self._prediction_columns.get_columns_list()
        else:
            prediction = []
        utility_columns = [
            col.column_name
            for col in [
                self._id_column,
                self._datetime_column,
                self._target,
                *prediction,
            ]
            if col is not None
        ]
        return [column for column in self._columns if _check_filter(column, utility_columns, filter_def)]

    def get_target_column(self) -> Optional[ColumnDefinition]:
        return self._target

    def get_prediction_columns(self) -> Optional[PredictionColumns]:
        return self._prediction_columns

    def get_id_column(self) -> Optional[ColumnDefinition]:
        return self._id_column

    def get_datetime_column(self) -> Optional[ColumnDefinition]:
        return self._datetime_column

    def task(self) -> Optional[str]:
        return self._task

    def classification_labels(self) -> Optional[Sequence[str]]:
        return self._classification_labels


def _process_column(
    column_name: Optional[str],
    data: _InputData,
    if_partially_present: str = "raise",
) -> Optional[ColumnDefinition]:
    if column_name is None:
        return None
    presense = _get_column_presence(column_name, data)
    if presense == ColumnPresenceState.Partially:
        if if_partially_present == "raise":
            raise ValueError(f"Column ({column_name}) is partially present in data")
        if if_partially_present == "skip":
            return None
        if if_partially_present == "keep":
            return ColumnDefinition(column_name, _get_column_type(column_name, data))
        return None
    if presense == ColumnPresenceState.Present:
        return ColumnDefinition(column_name, _get_column_type(column_name, data))
    return None


def _prediction_column(
    prediction: Optional[Union[str, int, Sequence[int], Sequence[str]]],
    target_type: Optional[ColumnType],
    target_names: Optional[List[str]],
    task: Optional[str],
    data: _InputData,
) -> Optional[PredictionColumns]:
    if prediction is None:
        return None
    if isinstance(prediction, str):
        prediction_present = _get_column_presence(prediction, data)
        if prediction_present == ColumnPresenceState.Missing:
            return None
        if prediction_present == ColumnPresenceState.Partially:
            raise ValueError(f"Prediction column ({prediction}) is partially present in data")
        prediction_type = _get_column_type(prediction, data)
        if task == TaskType.CLASSIFICATION_TASK:
            if prediction_type == ColumnType.Categorical:
                return PredictionColumns(predicted_values=ColumnDefinition(prediction, prediction_type))
            if prediction_type == ColumnType.Numerical:
                return PredictionColumns(prediction_probas=[ColumnDefinition(prediction, prediction_type)])
            raise ValueError(f"Unexpected type for prediction column ({prediction}) (it is {prediction_type})")
        if task == TaskType.REGRESSION_TASK:
            if prediction_type == ColumnType.Categorical:
                raise ValueError("Prediction type is categorical but task is regression")
            if prediction_type == ColumnType.Numerical:
                return PredictionColumns(predicted_values=ColumnDefinition(prediction, prediction_type))
        if task is None:
            if prediction_type == ColumnType.Numerical and target_type == ColumnType.Categorical:
                # probably this is binary with single column of probabilities
                return PredictionColumns(prediction_probas=[ColumnDefinition(prediction, prediction_type)])
            return PredictionColumns(predicted_values=ColumnDefinition(prediction, prediction_type))
    if isinstance(prediction, list):
        if target_names is not None:
            if prediction != target_names:
                raise ValueError("List of prediction columns should be equal to target_names if both set")
        presence = [_get_column_presence(column, data) for column in prediction]
        if all([item == ColumnPresenceState.Missing for item in presence]):
            return None
        if all([item == ColumnPresenceState.Present for item in presence]):
            prediction_defs = [ColumnDefinition(column, _get_column_type(column, data)) for column in prediction]
            if any([item.column_type != ColumnType.Numerical for item in prediction_defs]):
                raise ValueError(f"Some prediction columns have incorrect types {prediction_defs}")
            return PredictionColumns(prediction_probas=prediction_defs)
    raise ValueError("Unexpected type for prediction field in column_mapping")


def _filter_by_type(column: Optional[ColumnDefinition], column_type: ColumnType, exclude: List[str]) -> bool:
    return column is not None and column.column_type == column_type and column.column_name not in exclude


def create_data_definition(
    reference_data: Optional[pd.DataFrame],
    current_data: pd.DataFrame,
    mapping: ColumnMapping,
) -> DataDefinition:
    data = _InputData(reference_data, current_data)
    id_column = _process_column(mapping.id, data)
    target_column = _process_column(mapping.target, data)
    datetime_column = _process_column(mapping.datetime, data)

    prediction_columns = _prediction_column(
        mapping.prediction,
        target_column.column_type if target_column is not None else None,
        mapping.target_names,
        mapping.task,
        data,
    )

    prediction_cols = prediction_columns.get_columns_list() if prediction_columns is not None else []
    all_columns = [
        id_column,
        datetime_column,
        target_column,
        *prediction_cols,
    ]
    utility_column_names = [column.column_name for column in all_columns if column is not None]
    data_columns = set(data.current.columns) | (set(data.reference.columns) if data.reference is not None else set())
    col_defs = [_process_column(column_name, data, if_partially_present="skip") for column_name in data_columns]

    if mapping.numerical_features is None:
        num = [column for column in col_defs if _filter_by_type(column, ColumnType.Numerical, utility_column_names)]
        all_columns.extend(num)
    else:
        all_columns.extend(
            [
                _process_column(column_name, data)
                for column_name in mapping.numerical_features
                if column_name not in utility_column_names
            ]
        )

    if mapping.categorical_features is None:
        cat = [column for column in col_defs if _filter_by_type(column, ColumnType.Categorical, utility_column_names)]
        all_columns.extend(cat)
    else:
        all_columns.extend(
            [
                _process_column(column_name, data)
                for column_name in mapping.categorical_features
                if column_name not in utility_column_names
            ]
        )

    if mapping.datetime_features is None:
        dt = [column for column in col_defs if _filter_by_type(column, ColumnType.Datetime, utility_column_names)]
        all_columns.extend(dt)
    else:
        all_columns.extend(
            [
                _process_column(column_name, data)
                for column_name in mapping.datetime_features
                if column_name not in utility_column_names
            ]
        )

    task = mapping.task
    if task is None:
        if target_column is None:
            task = None
        elif target_column.column_type == ColumnType.Categorical:
            task = TaskType.CLASSIFICATION_TASK
        elif target_column.column_type == ColumnType.Numerical:
            task = TaskType.REGRESSION_TASK
        else:
            task = None

    return DataDefinition(
        columns=[col for col in all_columns if col is not None],
        id_column=id_column,
        datetime_column=datetime_column,
        target=target_column,
        prediction_columns=prediction_columns,
        task=task,
        classification_labels=mapping.target_names,
    )


class ColumnPresenceState(Enum):
    Present = 0
    Partially = 1
    Missing = 2


def _get_column_presence(column_name: str, data: _InputData) -> ColumnPresenceState:
    if column_name in data.current.columns:
        if data.reference is None or column_name in data.reference.columns:
            return ColumnPresenceState.Present
        return ColumnPresenceState.Partially
    if data.reference is None or column_name not in data.reference.columns:
        return ColumnPresenceState.Missing
    return ColumnPresenceState.Partially


NUMBER_UNIQUE_AS_CATEGORICAL = 5


def _get_column_type(column_name: str, data: _InputData) -> ColumnType:
    ref_type = None
    ref_unique = None
    if data.reference is not None and column_name in data.reference.columns:
        ref_type = data.reference[column_name].dtype
        ref_unique = data.reference[column_name].nunique()
    cur_type = None
    cur_unique = None
    if column_name in data.current.columns:
        cur_type = data.current[column_name].dtype
        cur_unique = data.current[column_name].nunique()
    if (
        ref_type is not None
        and cur_type is not None
        and (ref_type != cur_type and not np.can_cast(cur_type, ref_type) and not np.can_cast(ref_type, cur_type))
    ):
        raise ValueError(f"Column {column_name} have different types in reference {ref_type} and current {cur_type}")
    if pd.api.types.is_integer_dtype(cur_type if cur_type is not None else ref_type):
        nunique = ref_unique or cur_unique
        if nunique is not None and nunique <= NUMBER_UNIQUE_AS_CATEGORICAL:
            return ColumnType.Categorical
        return ColumnType.Numerical
    if pd.api.types.is_numeric_dtype(cur_type if cur_type is not None else ref_type):
        return ColumnType.Numerical
    if pd.api.types.is_datetime64_dtype(cur_type if cur_type is not None else ref_type):
        return ColumnType.Datetime
    return ColumnType.Categorical
