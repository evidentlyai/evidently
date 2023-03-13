from dataclasses import dataclass
from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence
from typing import Union

import numpy as np
import pandas as pd


@dataclass
class Distribution:
    x: Union[np.ndarray, list]
    y: Union[np.ndarray, list]


@dataclass
class ConfusionMatrix:
    labels: Sequence[Union[int, str]]
    values: list


@dataclass
class PredictionData:
    predictions: pd.Series
    prediction_probas: Optional[pd.DataFrame]
    labels: List[Union[str, int]]


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
    target_type: Optional[str]
    num_feature_names: List[str]
    cat_feature_names: List[str]
    text_feature_names: List[str]
    datetime_feature_names: List[str]
    target_names: Optional[Dict[Union[str, int], str]]
    task: Optional[str]

    def as_dict(self) -> Dict[str, Union[str, Optional[List[str]], Dict]]:
        return {
            "utility_columns": self.utility_columns.as_dict(),
            "cat_feature_names": self.cat_feature_names,
            "num_feature_names": self.num_feature_names,
            "datetime_feature_names": self.datetime_feature_names,
            "target_names": self.target_names,
            "text_feature_names": self.text_feature_names,
        }

    def get_all_features_list(self, cat_before_num: bool = True, include_datetime_feature: bool = False) -> List[str]:
        """List all features names.

        By default, returns cat features than num features and du not return other.

        If you want to change the order - set  `cat_before_num` to False.

        If you want to add date time columns - set `include_datetime_feature` to True.
        """
        if cat_before_num:
            result = self.cat_feature_names + self.num_feature_names + self.text_feature_names

        else:
            result = self.num_feature_names + self.cat_feature_names + self.text_feature_names

        if include_datetime_feature and self.datetime_feature_names:
            result += self.datetime_feature_names

        return result

    def get_all_columns_list(self, skip_id_column: bool = False, skip_text_columns: bool = False) -> List[str]:
        """List all columns."""
        result: List[str] = self.cat_feature_names + self.num_feature_names

        if not skip_text_columns:
            result.extend(self.text_feature_names)

        result.extend(
            [
                name
                for name in (
                    self.utility_columns.id_column if not skip_id_column else None,
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

        return (
            len(self.num_feature_names) + len(self.cat_feature_names) + len(self.text_feature_names) + len_time_columns
        )


ScatterData = Union[pd.Series, List[float], pd.Index]
ColumnScatter = Dict[str, ScatterData]


def column_scatter_from_df(df: pd.DataFrame, with_index: bool) -> ColumnScatter:
    data = {column: df[column] for column in df.columns}
    if with_index:
        data["index"] = df.index
    return data
