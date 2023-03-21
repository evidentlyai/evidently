from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence
from typing import Union

import numpy as np
import pandas as pd

from evidently.base_metric import MetricResult
from evidently.base_metric import MetricResultField
from evidently.pipeline.column_mapping import TargetNames

Label = Union[int, str]
ScatterData = Union[pd.Series, List[float], pd.Index]
ColumnScatter = Dict[Label, ScatterData]


class Distribution(MetricResultField):
    class Config:
        dict_include = False
        pd_include = False

    x: Union[np.ndarray, list, pd.Categorical, pd.Series]
    y: Union[np.ndarray, list, pd.Categorical, pd.Series]


class ConfusionMatrix(MetricResultField):
    class Config:
        smart_union = True

    labels: Sequence[Label]
    values: list  # todo better typing


class PredictionData(MetricResultField):
    class Config:
        dict_include = False

    predictions: pd.Series
    prediction_probas: Optional[pd.DataFrame]
    labels: List[Label]


class StatsByFeature(MetricResultField):
    class Config:
        dict_include = False
        pd_include = False

    plot_data: pd.DataFrame  # todo what type of plot?
    predictions: Optional[PredictionData]


class DatasetUtilityColumns(MetricResultField):
    date: Optional[str]
    id: Optional[str]
    target: Optional[str]
    prediction: Optional[Union[str, Sequence[str]]]


class DatasetColumns(MetricResultField):
    class Config:
        dict_exclude_fields = {"task", "target_type"}

    utility_columns: DatasetUtilityColumns
    target_type: Optional[str]
    num_feature_names: List[str]
    cat_feature_names: List[str]
    text_feature_names: List[str]
    datetime_feature_names: List[str]
    target_names: Optional[TargetNames]
    task: Optional[str]

    @property
    def target_names_list(self) -> Optional[List]:
        if isinstance(self.target_names, dict):
            return list(self.target_names.keys())
        return self.target_names

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
                    self.utility_columns.id if not skip_id_column else None,
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


def df_from_column_scatter(value: ColumnScatter) -> pd.DataFrame:
    df = pd.DataFrame.from_dict(value)
    if "index" in df.columns:
        df.set_index("index", inplace=True)
    return df


def column_scatter_from_df(df: pd.DataFrame, with_index: bool) -> ColumnScatter:
    data = {column: df[column] for column in df.columns}
    if with_index:
        data["index"] = df.index
    return data


class ScatterField(MetricResultField):
    class Config:
        smart_union = True
        dict_include = False
        pd_include = False

    scatter: ColumnScatter
    x_name: str
    plot_shape: Dict[str, float]


class ColumnScatterResult(MetricResult):
    class Config:
        smart_union = True
        dict_include = False

    current: ColumnScatter
    reference: Optional[ColumnScatter]
    x_name: str


PlotData = List[float]


class Boxes(MetricResultField):
    class Config:
        dict_include = False

    mins: PlotData
    lowers: PlotData
    means: PlotData
    uppers: PlotData
    maxs: PlotData


class RatesPlotData(MetricResultField):
    class Config:
        dict_include = False

    thrs: PlotData
    tpr: PlotData
    fpr: PlotData
    fnr: PlotData
    tnr: PlotData


class PRCurveData(MetricResultField):
    class Config:
        dict_include = False

    pr: PlotData
    rcl: PlotData
    thrs: PlotData


PRCurve = Dict[Label, PRCurveData]


class ROCCurveData(MetricResultField):
    class Config:
        dict_include = False

    fpr: PlotData
    tpr: PlotData
    thrs: PlotData


ROCCurve = Dict[Label, ROCCurveData]


class HistogramData(MetricResultField):
    class Config:
        dict_include = False

    x: pd.Series
    count: pd.Series
    name: Optional[str] = None

    @classmethod
    def from_df(cls, value: Optional[pd.DataFrame]):
        if value is None:
            return None
        return cls(x=value["x"], count=value["count"])

    @classmethod
    def from_distribution(cls, dist: Optional[Distribution], name: str = None):
        if dist is None:
            return None
        return cls(x=pd.Series(dist.x), count=pd.Series(dist.y), name=name)

    def to_df(self):
        return pd.DataFrame.from_dict(self.dict(include={"x", "count"}))


class Histogram(MetricResultField):
    class Config:
        dict_include = False

    current: HistogramData
    reference: Optional[HistogramData]

    current_log: Optional[HistogramData] = None
    reference_log: Optional[HistogramData] = None


# todo need better config overriding logic in metricresult
class DistributionIncluded(Distribution):
    class Config:
        dict_include = True


class ColumnCorrelations(MetricResultField):
    column_name: str
    kind: str
    values: DistributionIncluded


class DatasetClassificationQuality(MetricResultField):
    accuracy: float
    precision: float
    recall: float
    f1: float
    roc_auc: Optional[float] = None
    log_loss: Optional[float] = None
    tpr: Optional[float] = None
    tnr: Optional[float] = None
    fpr: Optional[float] = None
    fnr: Optional[float] = None
    rate_plots_data: Optional[RatesPlotData] = None
    plot_data: Optional[Boxes] = None
