from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence
from typing import Union

import numpy as np
import pandas as pd
from dataclasses import dataclass

from evidently.pipeline.column_mapping import ColumnMapping


@dataclass
class DatasetUtilityColumns:
    date: Optional[str]
    id_column: Optional[str]
    target: Optional[str]
    prediction: Optional[Union[str, Sequence[str]]]

    def as_dict(self) -> Dict[str, Union[Optional[str], Optional[Union[str, Sequence[str]]]]]:
        return {
            "date": self.date,
            "id": self.id_column,
            "target": self.target,
            "prediction": self.prediction,
        }


@dataclass
class DatasetColumns:
    utility_columns: DatasetUtilityColumns
    num_feature_names: List[str]
    cat_feature_names: List[str]
    datetime_feature_names: List[str]
    target_names: Optional[List[str]]

    def as_dict(self) -> Dict[str, Union[Optional[List[str]], Dict]]:
        return {
            "utility_columns": self.utility_columns.as_dict(),
            "cat_feature_names": self.cat_feature_names,
            "num_feature_names": self.num_feature_names,
            "datetime_feature_names": self.datetime_feature_names,
            "target_names": self.target_names,
        }

    def get_all_features_list(self, cat_before_num: bool = True, include_datetime_feature: bool = False) -> List[str]:
        """List all features names.

        By default, returns cat features than num features and du not return other.

        If you want to change the order - set  `cat_before_num` to False.

        If you want to add date time columns - set `include_datetime_feature` to True.
        """
        if cat_before_num:
            result = self.cat_feature_names + self.num_feature_names

        else:
            result = self.num_feature_names + self.cat_feature_names

        if include_datetime_feature and self.datetime_feature_names:
            result += self.datetime_feature_names

        return result

    def get_all_columns_list(self) -> List[str]:
        """List all columns."""
        result: List[str] = self.cat_feature_names + self.num_feature_names
        result.extend(
            [
                name
                for name in (
                    self.utility_columns.id_column,
                    self.utility_columns.date,
                    self.utility_columns.target,
                    self.utility_columns.prediction,
                )
                if name is not None and isinstance(name, str)
            ]
        )
        return result

    def get_features_len(self, include_time_columns: bool = False) -> int:
        """How mane feature do we have. It is useful for pagination in widgets.

        By default, we sum category nad numeric features.

        If you want to include date time columns - set `include_datetime_feature` to True.
        """
        if include_time_columns and self.datetime_feature_names:
            len_time_columns = len(self.datetime_feature_names)

        else:
            len_time_columns = 0

        return len(self.num_feature_names) + len(self.cat_feature_names) + len_time_columns


def process_columns(dataset: pd.DataFrame, column_mapping: ColumnMapping) -> DatasetColumns:
    if column_mapping is None:
        # data mapping should not be empty in this step
        raise ValueError("column_mapping should be present")
    date_column = column_mapping.datetime if column_mapping.datetime in dataset else None
    # index column name
    id_column = column_mapping.id
    target_column = column_mapping.target if column_mapping.target in dataset else None
    prediction_column = column_mapping.prediction
    num_feature_names = column_mapping.numerical_features
    cat_feature_names = column_mapping.categorical_features
    datetime_feature_names = column_mapping.datetime_features
    target_names = column_mapping.target_names
    utility_columns = [date_column, id_column, target_column]

    if isinstance(prediction_column, str):
        if prediction_column in dataset:
            prediction_column = prediction_column

        else:
            prediction_column = None

        utility_columns.append(prediction_column)

    elif prediction_column is None:
        pass

    else:
        prediction_column = dataset[prediction_column].columns.tolist()

        if prediction_column:
            utility_columns += prediction_column

    utility_columns_set = set(utility_columns)
    cat_feature_names_set = set(cat_feature_names or [])

    if num_feature_names is None:
        # try to guess about numeric features in the dataset
        # ignore prediction, target, index and explicitly specified category columns
        num_feature_names = sorted(
            list(set(dataset.select_dtypes([np.number]).columns) - utility_columns_set - cat_feature_names_set)
        )

    else:
        empty_cols = dataset[num_feature_names].isnull().mean()
        empty_cols = empty_cols[empty_cols == 1.].index
        num_feature_names = sorted(
            list(
                set(dataset[num_feature_names].select_dtypes([np.number]).columns).union(set(empty_cols))
            )
        )

    if datetime_feature_names is None:
        datetime_feature_names = sorted(list(set(dataset.select_dtypes(["datetime"]).columns) - utility_columns_set))
    else:
        empty_cols = dataset[datetime_feature_names].isnull().mean()
        empty_cols = empty_cols[empty_cols == 1.].index
        datetime_feature_names = sorted(
            list(
                set(dataset[datetime_feature_names].select_dtypes(["datetime"]).columns).union(set(empty_cols))
            )
        )

    cat_feature_names = column_mapping.categorical_features

    if cat_feature_names is None:
        cat_feature_names = sorted(
            list(set(dataset.select_dtypes(exclude=[np.number, "datetime"]).columns) - utility_columns_set)
        )

    else:
        cat_feature_names = dataset[cat_feature_names].columns.tolist()

    return DatasetColumns(
        DatasetUtilityColumns(date_column, id_column, target_column, prediction_column),
        num_feature_names or [],
        cat_feature_names or [],
        datetime_feature_names or [],
        target_names,
    )


def calculate_confusion_by_classes(confusion_matrix: pd.DataFrame, class_names: List[str]) -> Dict[str, Dict[str, int]]:
    """Calculate metrics
        TP (true positive)
        TN (true negative)
        FP (false positive)
        FN (false negative)
    for each class from confusion matrix.

    Returns a dict like:
    {
        "class_1_name": {
            "tp": 1,
            "tn": 5,
            "fp": 0,
            "fn": 3,
        },
        ...
    }
    """
    true_positive = np.diag(confusion_matrix)
    false_positive = confusion_matrix.sum(axis=0) - np.diag(confusion_matrix)
    false_negative = confusion_matrix.sum(axis=1) - np.diag(confusion_matrix)
    true_negative = confusion_matrix.sum() - (false_positive + false_negative + true_positive)
    confusion_by_classes = {}

    for idx, class_name in enumerate(class_names):
        confusion_by_classes[str(class_name)] = {
            "tp": true_positive[idx],
            "tn": true_negative[idx],
            "fp": false_positive[idx],
            "fn": false_negative[idx],
        }

    return confusion_by_classes


def recognize_task(target_name: str, reference_data: pd.DataFrame) -> str:
    """Try to guess about the target type:
    if the target has a numeric type and number of unique values > 5: task == ‘regression’
    in all other cases task == ‘classification’.

    Args:
        target_name: name of target column.
        reference_data: usually the data which you used in training.

    Returns:
        Task parameter.
    """
    if pd.api.types.is_numeric_dtype(reference_data[target_name]) and reference_data[target_name].nunique() >= 5:
        task = "regression"

    else:
        task = "classification"

    return task
