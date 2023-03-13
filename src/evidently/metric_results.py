import dataclasses
from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence
from typing import Union

import numpy as np
import pandas as pd
from pydantic import BaseModel

from evidently.base_metric import MetricResultField
from evidently.objects import ColumnScatter


class FromDataclassMixin(BaseModel):
    @classmethod
    def from_dataclass(cls, value):
        if value is None:
            return None
        return cls(**dataclasses.asdict(value))


class DistributionField(MetricResultField, FromDataclassMixin):
    class Config:
        dict_include = False
        pd_include = False

    x: Union[np.ndarray, list, pd.Categorical, pd.Series]
    y: Union[np.ndarray, list, pd.Categorical, pd.Series]


class ConfusionMatrixField(MetricResultField, FromDataclassMixin):
    labels: Union[Sequence[int], Sequence[str]]  # Sequence[Union[int, str]]
    values: list  # todo better typing


class PredictionDataField(MetricResultField, FromDataclassMixin):
    predictions: pd.Series
    prediction_probas: Optional[pd.DataFrame]
    labels: List[Union[str, int]]


class StatsByFeature(MetricResultField):
    class Config:
        dict_include = False
        pd_include = False

    plot_data: pd.DataFrame  # todo what type of plot?
    predictions: Optional[PredictionDataField]


class DatasetUtilityColumnsField(MetricResultField):
    date: Optional[str]
    id_column: Optional[str]
    target: Optional[str]
    prediction: Optional[Union[str, Sequence[str]]]


class DatasetColumnsField(MetricResultField, FromDataclassMixin):
    utility_columns: DatasetUtilityColumnsField
    target_type: Optional[str]
    num_feature_names: List[str]
    cat_feature_names: List[str]
    text_feature_names: List[str]
    datetime_feature_names: List[str]
    target_names: Optional[Dict[Union[str, int], str]]
    task: Optional[str]

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


class ScatterField(MetricResultField):
    class Config:
        dict_include = False
        pd_include = False

    scatter: ColumnScatter
    x_name: str
    plot_shape: Dict[str, float]
