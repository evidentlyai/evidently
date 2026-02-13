from typing import ClassVar
from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence
from typing import Set
from typing import Tuple
from typing import Type
from typing import TypeVar
from typing import Union
from typing import overload

import pandas as pd
from pydantic import TypeAdapter
from pydantic.v1 import validator
from typing_extensions import Literal

from evidently.legacy.base_metric import MetricResult
from evidently.legacy.core import IncludeTags
from evidently.legacy.core import Label
from evidently.legacy.core import PydanticNPArray
from evidently.legacy.core import pydantic_type_validator
from evidently.legacy.pipeline.column_mapping import TargetNames

try:
    List.__getitem__.__closure__[0].cell_contents.cache_clear()  # type: ignore
except AttributeError:  # since python 3.12
    from typing import _caches  # type: ignore[attr-defined]

    _caches[List.__getitem__.__wrapped__].cache_clear()  # type: ignore[attr-defined]

LabelList = List[Label]


class _LabelKeyType(int):
    pass


LabelKey = Union[_LabelKeyType, Label]  # type: ignore[valid-type]


@pydantic_type_validator(_LabelKeyType)
def label_key_valudator(value):
    try:
        return int(value)
    except ValueError:
        return value


ScatterData = Union[pd.Series]
ContourData = Tuple[PydanticNPArray, List[float], List[float]]
ColumnScatter = Dict[LabelKey, ScatterData]

ScatterAggData = Union[pd.DataFrame]
ColumnAggScatter = Dict[LabelKey, ScatterAggData]


class _ColumnScatterOrAggType:
    pass


ColumnScatterOrAgg = Union[_ColumnScatterOrAggType, ColumnScatter, ColumnAggScatter]  # type: ignore[valid-type]


@pydantic_type_validator(_ColumnScatterOrAggType)
def column_scatter_valudator(value):
    if any(isinstance(o, dict) for o in value.values()):
        # dict -> dataframe -> agg
        return TypeAdapter(ColumnAggScatter).validate_python(value)
    if any(isinstance(o, (pd.DataFrame, pd.Series)) for o in value.values()):
        return value
    return TypeAdapter(ColumnScatter).validate_python(value)


class Distribution(MetricResult):
    __pd_include__: ClassVar[bool] = False
    __tags__: ClassVar[Set[IncludeTags]] = {IncludeTags.Render}
    __extract_as_obj__: ClassVar[bool] = True
    __type_alias__: ClassVar[Optional[str]] = "evidently:metric_result:Distribution"

    x: Union[PydanticNPArray, list, pd.Categorical, pd.Series]
    y: Union[PydanticNPArray, list, pd.Categorical, pd.Series]


class ConfusionMatrix(MetricResult):
    __field_tags__: ClassVar[Dict[str, set]] = {"labels": {IncludeTags.Parameter}}
    __type_alias__: ClassVar[Optional[str]] = "evidently:metric_result:ConfusionMatrix"

    labels: Sequence[Label]
    values: list  # todo better typing


class PredictionData(MetricResult):
    __dict_include__: ClassVar[bool] = False
    __type_alias__: ClassVar[Optional[str]] = "evidently:metric_result:PredictionData"

    predictions: pd.Series
    labels: LabelList
    prediction_probas: Optional[pd.DataFrame] = None

    @validator("prediction_probas")
    def validate_prediction_probas(cls, value: pd.DataFrame, values):
        """Align label types"""
        if value is None:
            return None
        labels = values["labels"]
        for col in list(value.columns):
            if col not in labels:
                if str(col) in labels:
                    value.rename(columns={col: str(col)}, inplace=True)
                    continue
                try:
                    int_col = int(col)
                    if int_col in labels:
                        value.rename(columns={col: int_col}, inplace=True)
                except ValueError:
                    pass
        return value


class StatsByFeature(MetricResult):
    __dict_include__: ClassVar[bool] = False
    __pd_include__: ClassVar[bool] = False
    __tags__: ClassVar[Set[IncludeTags]] = {IncludeTags.Render}
    __type_alias__: ClassVar[Optional[str]] = "evidently:metric_result:StatsByFeature"

    plot_data: pd.DataFrame  # todo what type of plot?
    predictions: Optional[PredictionData] = None


class DatasetUtilityColumns(MetricResult):
    __type_alias__: ClassVar[Optional[str]] = "evidently:metric_result:DatasetUtilityColumns"

    date: Optional[str] = None
    id: Optional[str] = None
    target: Optional[str] = None
    prediction: Optional[Union[str, Sequence[str]]] = None


class DatasetColumns(MetricResult):
    __dict_exclude_fields__: ClassVar[set] = {"task", "target_type"}
    __pd_include__: ClassVar[bool] = False
    __tags__: ClassVar[Set[IncludeTags]] = {IncludeTags.Parameter}
    __type_alias__: ClassVar[Optional[str]] = "evidently:metric_result:DatasetColumns"

    utility_columns: DatasetUtilityColumns
    target_type: Optional[str] = None
    num_feature_names: List[str]
    cat_feature_names: List[str]
    text_feature_names: List[str]
    datetime_feature_names: List[str]
    target_names: Optional[TargetNames] = None
    task: Optional[str] = None

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


def column_scatter_from_df(df: Optional[pd.DataFrame], with_index: bool) -> Optional[ColumnScatter]:
    if df is None:
        return None
    data: ColumnScatter = {column: df[column] for column in df.columns}
    if with_index:
        data["index"] = df.index.to_series()
    return data


class ScatterAggField(MetricResult):
    __dict_include__: ClassVar[bool] = False
    __pd_include__: ClassVar[bool] = False
    __tags__: ClassVar[Set[IncludeTags]] = {IncludeTags.Render}
    __type_alias__: ClassVar[Optional[str]] = "evidently:metric_result:ScatterAggField"

    scatter: ColumnAggScatter
    x_name: str
    plot_shape: Dict[str, float]


class ScatterField(MetricResult):
    __dict_include__: ClassVar[bool] = False
    __pd_include__: ClassVar[bool] = False
    __tags__: ClassVar[Set[IncludeTags]] = {IncludeTags.Render}
    __type_alias__: ClassVar[Optional[str]] = "evidently:metric_result:ScatterField"

    scatter: ColumnScatter
    x_name: str
    plot_shape: Dict[str, float]


class ColumnScatterResult(MetricResult):
    __dict_include__: ClassVar[bool] = False
    __pd_include__: ClassVar[bool] = False
    __tags__: ClassVar[Set[IncludeTags]] = {IncludeTags.Render}
    __field_tags__: ClassVar[Dict[str, set]] = {"current": {IncludeTags.Current}, "reference": {IncludeTags.Reference}}
    __type_alias__: ClassVar[Optional[str]] = "evidently:metric_result:ColumnScatterResult"

    current: ColumnScatter
    reference: Optional[ColumnScatter] = None
    x_name: str
    x_name_ref: Optional[str] = None


class ColumnAggScatterResult(ColumnScatterResult):
    __field_tags__: ClassVar[Dict[str, set]] = {"current": {IncludeTags.Current}, "reference": {IncludeTags.Reference}}
    __type_alias__: ClassVar[Optional[str]] = "evidently:metric_result:ColumnAggScatterResult"

    # TODO: fix type collision with super type
    current: ColumnAggScatter  # type: ignore[assignment]
    reference: Optional[ColumnAggScatter] = None  # type: ignore[assignment]


PlotData = List[float]


class Boxes(MetricResult):
    __dict_include__: ClassVar[bool] = False
    __tags__: ClassVar[Set[IncludeTags]] = {IncludeTags.Render}
    __type_alias__: ClassVar[Optional[str]] = "evidently:metric_result:Boxes"

    mins: PlotData
    lowers: PlotData
    means: PlotData
    uppers: PlotData
    maxs: PlotData


class RatesPlotData(MetricResult):
    __dict_include__: ClassVar[bool] = False
    __tags__: ClassVar[Set[IncludeTags]] = {IncludeTags.Render}
    __type_alias__: ClassVar[Optional[str]] = "evidently:metric_result:RatesPlotData"

    thrs: PlotData
    tpr: PlotData
    fpr: PlotData
    fnr: PlotData
    tnr: PlotData


class PRCurveData(MetricResult):
    __dict_include__: ClassVar[bool] = False
    __tags__: ClassVar[Set[IncludeTags]] = {IncludeTags.Render}
    __type_alias__: ClassVar[Optional[str]] = "evidently:metric_result:PRCurveData"

    pr: PlotData
    rcl: PlotData
    thrs: PlotData


PRCurve = Dict[Label, PRCurveData]


class ROCCurveData(MetricResult):
    __dict_include__: ClassVar[bool] = False
    __tags__: ClassVar[Set[IncludeTags]] = {IncludeTags.Render}
    __type_alias__: ClassVar[Optional[str]] = "evidently:metric_result:ROCCurveData"

    fpr: PlotData
    tpr: PlotData
    thrs: PlotData


ROCCurve = Dict[Label, ROCCurveData]


class LiftCurveData(MetricResult):
    __dict_include__: ClassVar[bool] = False
    __tags__: ClassVar[Set[IncludeTags]] = {IncludeTags.Render}
    __type_alias__: ClassVar[Optional[str]] = "evidently:metric_result:LiftCurveData"

    lift: PlotData
    top: PlotData
    count: PlotData
    prob: PlotData
    tp: PlotData
    fp: PlotData
    precision: PlotData
    recall: PlotData
    f1_score: PlotData
    max_lift: PlotData
    relative_lift: PlotData
    percent: PlotData


LiftCurve = Dict[Label, LiftCurveData]


class HistogramData(MetricResult):
    __dict_include__: ClassVar[bool] = False
    __tags__: ClassVar[Set[IncludeTags]] = {IncludeTags.Render}
    __extract_as_obj__: ClassVar[bool] = True
    __type_alias__: ClassVar[Optional[str]] = "evidently:metric_result:HistogramData"

    x: pd.Series
    count: pd.Series
    name: Optional[str] = None

    @classmethod
    def from_df(cls, value: pd.DataFrame, name: Optional[str] = None):
        return cls(x=value["x"], count=value["count"], name=name)

    @classmethod
    def from_distribution(cls, dist: Optional[Distribution], name: Optional[str] = None):
        if dist is None:
            return None
        return cls(x=pd.Series(dist.x), count=pd.Series(dist.y), name=name)

    @classmethod
    def from_dict(cls, data: Optional[Dict], name: Optional[str] = None):
        if data is None:
            return None
        return cls(x=pd.Series(data.keys()), count=pd.Series(data.values()), name=name)

    @classmethod
    def from_any(
        cls, value: Union[None, "HistogramData", pd.DataFrame, Distribution, Dict], name: Optional[str] = None
    ):
        if value is None:
            return None
        if isinstance(value, HistogramData):
            return value
        if isinstance(value, pd.DataFrame):
            return cls.from_df(value, name)
        if isinstance(value, Distribution):
            return cls.from_distribution(value, name)
        if isinstance(value, dict):
            return cls.from_dict(value, name)
        raise NotImplementedError(f"Cannot create {cls.__name__} from {value.__class__.__name__}")

    def to_df(self):
        return pd.DataFrame.from_dict(self.model_dump(include={"x", "count"}))


class Histogram(MetricResult):
    __dict_include__: ClassVar[bool] = False
    __tags__: ClassVar[Set[IncludeTags]] = {IncludeTags.Render}
    __field_tags__: ClassVar[Dict[str, set]] = {
        "current": {IncludeTags.Current},
        "reference": {IncludeTags.Reference},
        "current_log": {IncludeTags.Current},
        "reference_log": {IncludeTags.Reference},
    }
    __type_alias__: ClassVar[Optional[str]] = "evidently:metric_result:Histogram"

    current: HistogramData
    reference: Optional[HistogramData] = None

    current_log: Optional[HistogramData] = None
    reference_log: Optional[HistogramData] = None


# todo need better config overriding logic in metricresult
class DistributionIncluded(Distribution):
    __tags__: ClassVar[Set[IncludeTags]] = set()
    __dict_include__: ClassVar[bool] = True
    __field_tags__: ClassVar[Dict[str, set]] = {"x": {IncludeTags.Extra}}
    __type_alias__: ClassVar[Optional[str]] = "evidently:metric_result:DistributionIncluded"


class ColumnCorrelations(MetricResult):
    __field_tags__: ClassVar[Dict[str, set]] = {"column_name": {IncludeTags.Parameter}, "kind": {IncludeTags.Parameter}}
    __type_alias__: ClassVar[Optional[str]] = "evidently:metric_result:ColumnCorrelations"

    column_name: str
    kind: str
    values: DistributionIncluded

    def get_pandas(self) -> pd.DataFrame:
        return pd.DataFrame(
            [
                {"kind": self.kind, "column_name": key, "value": value}
                for key, value in zip(self.values.x, self.values.y)
            ]
        )


class DatasetClassificationQuality(MetricResult):
    __type_alias__: ClassVar[Optional[str]] = "evidently:metric_result:DatasetClassificationQuality"

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


TR = TypeVar("TR")
TA = TypeVar("TA")


@overload
def raw_agg_properties(
    field_name, raw_type: Type[TR], agg_type: Type[TA], optional: Literal[False]
) -> Tuple[TR, TA]: ...


@overload
def raw_agg_properties(
    field_name, raw_type: Type[TR], agg_type: Type[TA], optional: Literal[True]
) -> Tuple[Optional[TR], Optional[TA]]: ...


def raw_agg_properties(field_name, raw_type: Type[TR], agg_type: Type[TA], optional: bool) -> Tuple[TR, TA]:
    def property_raw(self):
        val = getattr(self, field_name)
        if optional and val is None:
            return None
        if isinstance(raw_type, type) and not isinstance(val, raw_type):
            raise ValueError("Raw data not available")
        return val

    def property_agg(self):
        val = getattr(self, field_name)
        if optional and val is None:
            return None
        if isinstance(agg_type, type) and not isinstance(val, agg_type):
            raise ValueError("Agg data not available")
        return val

    return property(property_raw), property(property_agg)  # type: ignore[return-value]
