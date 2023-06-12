"""Methods for overall dataset quality calculations - rows count, a specific values count, etc."""

import dataclasses
from typing import Callable
from typing import Collection
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency

from evidently.core import ColumnType
from evidently.metric_results import ColumnCorrelations
from evidently.metric_results import DatasetColumns
from evidently.metric_results import Distribution
from evidently.metric_results import Histogram
from evidently.metric_results import HistogramData
from evidently.utils.data_preprocessing import DataDefinition
from evidently.utils.types import ColumnDistribution
from evidently.utils.visualizations import get_gaussian_kde
from evidently.utils.visualizations import is_possible_contour
from evidently.utils.visualizations import make_hist_for_cat_plot
from evidently.utils.visualizations import make_hist_for_num_plot

MAX_CATEGORIES = 5


def get_rows_count(data: Union[pd.DataFrame, pd.Series]) -> int:
    """Count quantity of rows in  a dataset"""
    return data.shape[0]


@dataclasses.dataclass
class FeatureQualityStats:
    """Class for all features data quality metrics store.

    A type of the feature is stored in `feature_type` field.
    Concrete stat kit depends on the feature type. Is a metric is not applicable - leave `None` value for it.

    Metrics for all feature types:
        - feature type - cat for category, num for numeric, datetime for datetime features
        - count - quantity of a meaningful values (do not take into account NaN values)
        - missing_count - quantity of meaningless (NaN) values
        - missing_percentage - the percentage of the missed values
        - unique_count - quantity of unique values
        - unique_percentage - the percentage of the unique values
        - max - maximum value (not applicable for category features)
        - min - minimum value (not applicable for category features)
        - most_common_value - the most common value in the feature values
        - most_common_value_percentage - the percentage of the most common value
        - most_common_not_null_value - if `most_common_value` equals NaN - the next most common value. Otherwise - None
        - most_common_not_null_value_percentage - the percentage of `most_common_not_null_value` if it is defined.
            If `most_common_not_null_value` is not defined, equals None too.

    Metrics for numeric features only:
        - infinite_count - quantity infinite values (for numeric features only)
        - infinite_percentage - the percentage of infinite values (for numeric features only)
        - percentile_25 - 25% percentile for meaningful values
        - percentile_50 - 50% percentile for meaningful values
        - percentile_75 - 75% percentile for meaningful values
        - mean - the sum of the meaningful values divided by the number of the meaningful values
        - std - standard deviation of the values

    Metrics for category features only:
        - new_in_current_values_count - quantity of new values in the current dataset after the reference
            Defined for reference dataset only.
        - new_in_current_values_count - quantity of values in the reference dataset that not presented in the current
            Defined for reference dataset only.
    """

    # feature type - cat for category, num for numeric, datetime for datetime features
    feature_type: str
    # quantity on
    number_of_rows: int = 0
    count: int = 0
    infinite_count: Optional[int] = None
    infinite_percentage: Optional[float] = None
    missing_count: Optional[int] = None
    missing_percentage: Optional[float] = None
    unique_count: Optional[int] = None
    unique_percentage: Optional[float] = None
    percentile_25: Optional[float] = None
    percentile_50: Optional[float] = None
    percentile_75: Optional[float] = None
    max: Optional[Union[int, float, bool, str]] = None
    min: Optional[Union[int, float, bool, str]] = None
    mean: Optional[float] = None
    most_common_value: Optional[Union[int, float, bool, str]] = None
    most_common_value_percentage: Optional[float] = None
    std: Optional[float] = None
    most_common_not_null_value: Optional[Union[int, float, bool, str]] = None
    most_common_not_null_value_percentage: Optional[float] = None
    new_in_current_values_count: Optional[int] = None
    unused_in_current_values_count: Optional[int] = None

    def is_datetime(self):
        """Checks that the object store stats for a datetime feature"""
        return self.feature_type == "datetime"

    def is_numeric(self):
        """Checks that the object store stats for a numeric feature"""
        return self.feature_type == "num"

    def is_category(self):
        """Checks that the object store stats for a category feature"""
        return self.feature_type == "cat"

    def as_dict(self):
        return {field.name: getattr(self, field.name) for field in dataclasses.fields(FeatureQualityStats)}

    def __eq__(self, other):
        for field in dataclasses.fields(FeatureQualityStats):
            other_field_value = getattr(other, field.name)
            self_field_value = getattr(self, field.name)

            if pd.isnull(other_field_value) and pd.isnull(self_field_value):
                continue

            if not other_field_value == self_field_value:
                return False

        return True


@dataclasses.dataclass
class DataQualityStats:
    rows_count: int
    num_features_stats: Optional[Dict[str, FeatureQualityStats]] = None
    cat_features_stats: Optional[Dict[str, FeatureQualityStats]] = None
    datetime_features_stats: Optional[Dict[str, FeatureQualityStats]] = None
    target_stats: Optional[Dict[str, FeatureQualityStats]] = None
    prediction_stats: Optional[Dict[str, FeatureQualityStats]] = None

    def get_all_features(self) -> Dict[str, FeatureQualityStats]:
        result = {}

        for features in (
            self.target_stats,
            self.prediction_stats,
            self.datetime_features_stats,
            self.cat_features_stats,
            self.num_features_stats,
        ):
            if features is not None:
                result.update(features)

        return result

    def __getitem__(self, item) -> FeatureQualityStats:
        for features in (
            self.target_stats,
            self.prediction_stats,
            self.datetime_features_stats,
            self.cat_features_stats,
            self.num_features_stats,
        ):
            if features is not None and item in features:
                return features[item]

        raise KeyError(item)


def get_features_stats(feature: pd.Series, feature_type: ColumnType) -> FeatureQualityStats:
    def get_percentage_from_all_values(value: Union[int, float]) -> float:
        return np.round(100 * value / all_values_count, 2)

    result = FeatureQualityStats(feature_type=feature_type.value)
    all_values_count = feature.shape[0]

    if not all_values_count > 0:
        # we have no data, return default stats for en empty dataset
        return result
    result.number_of_rows = all_values_count
    result.missing_count = int(feature.isnull().sum())
    result.count = int(feature.count())
    all_values_count = feature.shape[0]
    value_counts = feature.value_counts(dropna=False)
    result.missing_percentage = np.round(100 * result.missing_count / all_values_count, 2)
    unique_count: int = feature.nunique()
    result.unique_count = unique_count
    result.unique_percentage = get_percentage_from_all_values(unique_count)
    result.most_common_value = value_counts.index[0]
    result.most_common_value_percentage = get_percentage_from_all_values(value_counts.iloc[0])

    if result.count > 0 and pd.isnull(result.most_common_value):
        result.most_common_not_null_value = value_counts.index[1]
        result.most_common_not_null_value_percentage = get_percentage_from_all_values(value_counts.iloc[1])

    if feature_type == ColumnType.Numerical:
        # round most common feature value for numeric features to 1e-5
        if not np.issubdtype(feature, np.number):
            feature = feature.astype(float)
        if isinstance(result.most_common_value, float):
            result.most_common_value = np.round(result.most_common_value, 5)
        result.infinite_count = int(np.sum(np.isinf(feature)))
        result.infinite_percentage = get_percentage_from_all_values(result.infinite_count)
        result.max = np.round(feature.max(), 2)
        result.min = np.round(feature.min(), 2)
        common_stats = dict(feature.describe())
        std = common_stats["std"]
        result.std = np.round(std, 2)
        result.mean = np.round(common_stats["mean"], 2)
        result.percentile_25 = np.round(common_stats["25%"], 2)
        result.percentile_50 = np.round(common_stats["50%"], 2)
        result.percentile_75 = np.round(common_stats["75%"], 2)

    if feature_type == ColumnType.Datetime:
        # cast datetime value to str for datetime features
        result.most_common_value = str(result.most_common_value)
        # cast datetime value to str for datetime features
        result.max = str(feature.max())
        result.min = str(feature.min())

    return result


def calculate_data_quality_stats(
    dataset: pd.DataFrame, columns: DatasetColumns, task: Optional[str]
) -> DataQualityStats:
    result = DataQualityStats(rows_count=get_rows_count(dataset))

    result.num_features_stats = {
        feature_name: get_features_stats(dataset[feature_name], feature_type=ColumnType.Numerical)
        for feature_name in columns.num_feature_names
    }

    result.cat_features_stats = {
        feature_name: get_features_stats(dataset[feature_name], feature_type=ColumnType.Categorical)
        for feature_name in columns.cat_feature_names
    }

    if columns.utility_columns.date:
        date_list = columns.datetime_feature_names + [columns.utility_columns.date]

    else:
        date_list = columns.datetime_feature_names

    result.datetime_features_stats = {
        feature_name: get_features_stats(dataset[feature_name], feature_type=ColumnType.Datetime)
        for feature_name in date_list
    }

    target_name = columns.utility_columns.target

    if target_name is not None and target_name in dataset:
        result.target_stats = {}

        if task == "classification":
            result.target_stats[target_name] = get_features_stats(
                dataset[target_name],
                feature_type=ColumnType.Categorical,
            )

        else:
            result.target_stats[target_name] = get_features_stats(
                dataset[target_name],
                feature_type=ColumnType.Numerical,
            )

    prediction_name = columns.utility_columns.prediction

    if isinstance(prediction_name, str) and prediction_name in dataset:
        result.prediction_stats = {}

        if task == "classification":
            result.prediction_stats[prediction_name] = get_features_stats(
                dataset[prediction_name],
                feature_type=ColumnType.Categorical,
            )

        else:
            result.prediction_stats[prediction_name] = get_features_stats(
                dataset[prediction_name],
                feature_type=ColumnType.Numerical,
            )

    return result


def _relabel_data(
    current_data: pd.Series,
    reference_data: Optional[pd.Series],
    max_categories: Optional[int] = MAX_CATEGORIES,
) -> Tuple[pd.Series, Optional[pd.Series]]:
    if max_categories is None:
        return current_data.copy(), reference_data.copy() if reference_data is not None else None

    current_data_str = current_data.astype(str)
    reference_data_str = None
    if reference_data is not None:
        reference_data_str = reference_data.astype(str)
        unique_values = len(
            np.union1d(
                current_data_str.unique(),
                reference_data_str.unique(),
            )
        )
    else:
        unique_values = current_data_str.nunique()

    if unique_values > max_categories:
        curr_cats = current_data_str.value_counts(normalize=True)

        if reference_data_str is not None:
            ref_cats = reference_data_str.value_counts(normalize=True)
            categories = pd.concat([curr_cats, ref_cats])

        else:
            categories = curr_cats

        cats = categories.sort_values(ascending=False).index.drop_duplicates(keep="first")[:max_categories].values

        result_current = current_data.apply(lambda x: x if str(x) in cats else "other")
        result_reference = None
        if reference_data is not None:
            result_reference = reference_data.apply(lambda x: x if str(x) in cats else "other")
        return result_current, result_reference
    else:
        return current_data.copy(), reference_data.copy() if reference_data is not None else None


def _split_periods(curr_data: pd.DataFrame, ref_data: pd.DataFrame, feature_name: str):
    max_ref_date = ref_data[feature_name].max()
    min_curr_date = curr_data[feature_name].min()

    if (
        curr_data.loc[curr_data[feature_name] == min_curr_date, "number_of_items"].iloc[0]
        > ref_data.loc[ref_data[feature_name] == max_ref_date, "number_of_items"].iloc[0]
    ):
        curr_data.loc[curr_data[feature_name] == min_curr_date, "number_of_items"] = (
            curr_data.loc[curr_data[feature_name] == min_curr_date, "number_of_items"]
            + ref_data.loc[ref_data[feature_name] == max_ref_date, "number_of_items"]
        )
        ref_data = ref_data[ref_data[feature_name] != max_ref_date]
    else:
        ref_data.loc[ref_data[feature_name] == max_ref_date, "number_of_items"] = (
            ref_data.loc[ref_data[feature_name] == max_ref_date, "number_of_items"]
            + curr_data.loc[curr_data[feature_name] == min_curr_date, "number_of_items"]
        )
        curr_data = curr_data[curr_data[feature_name] != min_curr_date]
    return curr_data, ref_data


def _choose_agg_period(
    current_date_column: pd.Series,
    reference_date_column: Optional[pd.Series],
) -> Tuple[str, str]:
    optimal_points = 150
    prefix_dict = {
        "A": "year",
        "Q": "quarter",
        "M": "month",
        "W": "week",
        "D": "day",
        "H": "hour",
    }
    datetime_feature = current_date_column
    if reference_date_column is not None:
        datetime_feature = pd.concat([datetime_feature, reference_date_column])
    days = (datetime_feature.max() - datetime_feature.min()).days
    time_points = pd.Series(
        index=["A", "Q", "M", "W", "D", "H"],
        data=[
            abs(optimal_points - days / 365),
            abs(optimal_points - days / 90),
            abs(optimal_points - days / 30),
            abs(optimal_points - days / 7),
            abs(optimal_points - days),
            abs(optimal_points - days * 24),
        ],
    )
    period_prefix = prefix_dict[time_points.idxmin()]
    return period_prefix, str(time_points.idxmin())


def prepare_data_for_plots(
    current_data: pd.Series,
    reference_data: Optional[pd.Series],
    column_type: ColumnType,
    max_categories: Optional[int] = MAX_CATEGORIES,
) -> Tuple[pd.Series, Optional[pd.Series]]:
    if column_type == ColumnType.Categorical:
        current_data, reference_data = _relabel_data(current_data, reference_data, max_categories)
    else:
        current_data = current_data.copy()
        if reference_data is not None:
            reference_data = reference_data.copy()
    return current_data, reference_data


def _transform_df_to_time_mean_view(
    period_data: pd.Series,
    datetime_column_name: str,
    datetime_data: pd.Series,
    data_column_name: str,
    column_data: pd.Series,
):
    df = pd.DataFrame({"period": period_data, data_column_name: column_data, datetime_column_name: datetime_data})
    df = df.groupby("period")[data_column_name].mean().reset_index()
    df[datetime_column_name] = df["period"].dt.to_timestamp()
    return df


def _transform_df_to_time_count_view(
    period_data: pd.Series,
    datetime_column_name: str,
    datetime_data: pd.Series,
    data_column_name: str,
    column_data: pd.Series,
):
    df = pd.DataFrame({"period": period_data, datetime_column_name: datetime_data, data_column_name: column_data})
    df = df.groupby(["period", data_column_name]).size()
    df.name = "num"
    df = df.reset_index()
    df[datetime_column_name] = df["period"].dt.to_timestamp()
    return df[df["num"] > 0]


Data = Tuple[str, ColumnType, pd.Series, Optional[pd.Series]]


def _prepare_box_data(
    curr: pd.DataFrame,
    ref: Optional[pd.DataFrame],
    cat_feature_name: str,
    num_feature_name: str,
) -> Dict[str, Dict[str, list]]:
    dfs = [curr]
    names = ["current"]
    if ref is not None:
        dfs.append(ref)
        names.append("reference")
    res = {}
    for df, name in zip(dfs, names):
        df_for_plot = df.groupby(cat_feature_name)[num_feature_name].quantile([0, 0.25, 0.5, 0.75, 1]).reset_index()
        df_for_plot.columns = [cat_feature_name, "q", num_feature_name]
        res_df = {}
        values = df_for_plot[cat_feature_name].unique()

        def _quantiles(qdf, value):
            return qdf[df_for_plot.q == value].set_index(cat_feature_name).loc[values, num_feature_name].tolist()

        res_df["mins"] = _quantiles(df_for_plot, 0)
        res_df["lowers"] = _quantiles(df_for_plot, 0.25)
        res_df["means"] = _quantiles(df_for_plot, 0.5)
        res_df["uppers"] = _quantiles(df_for_plot, 0.75)
        res_df["maxs"] = _quantiles(df_for_plot, 1)
        res_df["values"] = values
        res[name] = res_df
    return res


def _get_count_values(column_data: pd.Series, target_data: pd.Series, target_name: str, column_name: str):
    df = pd.DataFrame({target_name: target_data, column_name: column_data})
    df = df.groupby([target_name, column_name]).size()
    df.name = "count_objects"
    df = df.reset_index()
    return df[df["count_objects"] > 0]


def plot_data(
    data: Data,
    datetime_data: Optional[Data],
    target_data: Optional[Data],
    agg_data: bool,
    merge_small_categories: Optional[int] = MAX_CATEGORIES,
) -> Tuple[Optional[Histogram], Optional[Dict[str, Collection[str]]], Optional[Dict[str, Collection[str]]]]:
    """
    Args:
        data: Column data includes column name current and reference data (if present)
        datetime_data: Datetime data if present
        target_data: Target data if present
        merge_small_categories: Maximum of labels in categorical data what should be shown
    Returns:
        Histogram data or None
        TODO: add reason why should be returned None
    """
    column_name, column_type, current_data, reference_data = data
    if column_type == ColumnType.Categorical:
        current_data, reference_data = _relabel_data(current_data, reference_data, merge_small_categories)
    else:
        current_data = current_data.copy()
        if reference_data is not None:
            reference_data = reference_data.copy()
    current_data.dropna(inplace=True)
    if reference_data is not None:
        reference_data.dropna(inplace=True)

    data_hist = None
    if column_type == ColumnType.Numerical:
        data_hist = make_hist_for_num_plot(current_data, reference_data, calculate_log=True)
    elif column_type == ColumnType.Categorical:
        data_hist = make_hist_for_cat_plot(current_data, reference_data, dropna=True)
    elif column_type == ColumnType.Datetime:
        prefix, freq = _choose_agg_period(current_data, reference_data)
        curr_data = current_data.dt.to_period(freq=freq).value_counts().reset_index()
        curr_data.columns = ["x", "number_of_items"]
        curr_data["x"] = curr_data["x"].dt.to_timestamp()
        reference = None
        if reference_data is not None:
            ref_data = reference_data.dt.to_period(freq=freq).value_counts().reset_index()
            ref_data.columns = ["x", "number_of_items"]
            ref_data["x"] = ref_data["x"].dt.to_timestamp()
            max_ref_date = ref_data["x"].max()
            min_curr_date = curr_data["x"].min()
            if max_ref_date == min_curr_date:
                curr_data, ref_data = _split_periods(curr_data, ref_data, "x")
            reference = ref_data
            reference.columns = ["x", "count"]
        curr_data.columns = ["x", "count"]
        data_hist = Histogram(current=HistogramData.from_df(curr_data), reference=HistogramData.from_df(reference))
    elif column_type == ColumnType.Text:
        data_hist = None
    else:
        raise ValueError(f"Unsupported column type {column_type}")

    data_in_time = None
    if datetime_data is not None:
        datetime_name, _, datetime_current, datetime_reference = datetime_data
        prefix, freq = _choose_agg_period(datetime_current, datetime_reference)
        current_period_data = datetime_current.dt.to_period(freq=freq)
        df_for_time_plot_ref = None
        reference_period_data = None
        if reference_data is not None and datetime_reference is not None:
            reference_period_data = datetime_reference.dt.to_period(freq=freq)
        if column_type == ColumnType.Numerical:
            df_for_time_plot_curr = _transform_df_to_time_mean_view(
                current_period_data,
                datetime_name,
                datetime_current,
                column_name,
                current_data,
            )
            if reference_period_data is not None:
                df_for_time_plot_ref = _transform_df_to_time_mean_view(
                    reference_period_data,
                    datetime_name,
                    datetime_reference,
                    column_name,
                    reference_data,
                )
            data_in_time = {
                "data_for_plots": {
                    "current": df_for_time_plot_curr,
                    "reference": df_for_time_plot_ref,
                },
                "freq": prefix,
                "datetime_name": datetime_name,
            }

        if column_type == ColumnType.Categorical:
            df_for_time_plot_curr = _transform_df_to_time_count_view(
                current_period_data,
                datetime_name,
                datetime_current,
                column_name,
                current_data,
            )
            if reference_period_data is not None:
                df_for_time_plot_ref = _transform_df_to_time_count_view(
                    reference_period_data,
                    datetime_name,
                    datetime_reference,
                    column_name,
                    reference_data,
                )
            data_in_time = {
                "data_for_plots": {
                    "current": df_for_time_plot_curr,
                    "reference": df_for_time_plot_ref,
                },
                "freq": prefix,
                "datetime_name": datetime_name,
            }

    data_by_target = None
    if target_data is not None:
        target_name, target_type, target_current, target_reference = target_data
        curr_df = pd.DataFrame({column_name: current_data, target_name: target_current})
        ref_df = None
        if target_reference is not None and reference_data is not None:
            ref_df = pd.DataFrame({column_name: reference_data, target_name: target_reference})
        if column_type == ColumnType.Categorical and target_type == ColumnType.Numerical:
            data_by_target = {
                "data_for_plots": _prepare_box_data(curr_df, ref_df, column_name, target_name),
                "target_name": target_name,
                "target_type": target_type.value,
            }
        if column_type == ColumnType.Numerical and target_type == ColumnType.Categorical:
            data_by_target = {
                "data_for_plots": _prepare_box_data(curr_df, ref_df, target_name, column_name),
                "target_name": target_name,
                "target_type": target_type.value,
            }
        if column_type == ColumnType.Numerical and target_type == ColumnType.Numerical:
            if (
                not agg_data
                or not is_possible_contour(target_current.loc[current_data.index], current_data)
                or (
                    reference_data is not None
                    and target_reference is not None
                    and not is_possible_contour(target_reference.loc[reference_data.index], reference_data)
                )
            ):
                result = {
                    "current": {
                        column_name: current_data.tolist(),
                        target_name: target_current.tolist(),
                    }
                }
                if reference_data is not None and target_reference is not None:
                    result["reference"] = {
                        column_name: reference_data.tolist(),
                        target_name: target_reference.tolist(),
                    }

            else:
                result = {"current": get_gaussian_kde(target_current.loc[current_data.index], current_data)}
                if reference_data is not None and target_reference is not None:
                    result["reference"] = get_gaussian_kde(target_reference.loc[reference_data.index], reference_data)

            data_by_target = {
                "data_for_plots": result,
                "target_name": target_name,
                "target_type": target_type.value,
            }

        if column_type == ColumnType.Categorical and target_type == ColumnType.Categorical:
            result = {"current": _get_count_values(current_data, target_current, target_name, column_name)}
            if target_reference is not None and reference_data is not None:
                result["reference"] = _get_count_values(reference_data, target_reference, target_name, column_name)
            data_by_target = {
                "data_for_plots": result,
                "target_name": target_name,
                "target_type": target_type.value,
            }

    return data_hist, data_in_time, data_by_target


def _select_features_for_corr(dataset: pd.DataFrame, data_definition: DataDefinition) -> tuple:
    """Define which features should be used for calculating correlation matrices:
        - for pearson, spearman, and kendall correlation matrices we select numerical features which have > 1
            unique values;
        - for kramer_v correlation matrix, we select categorical features which have > 1 unique values.
    Args:
        dataset: data for processing
        data_definition: definition for all columns in data
    Returns:
        num_for_corr: list of feature names for pearson, spearman, and kendall correlation matrices.
        cat_for_corr: list of feature names for kramer_v correlation matrix.
    """

    num = data_definition.get_columns("numerical_columns")
    cat = data_definition.get_columns("categorical_columns")
    num_for_corr = []
    cat_for_corr = []

    for col in num:
        col_name = col.column_name
        unique_count = dataset[col_name].nunique()
        if unique_count and unique_count > 1:
            num_for_corr.append(col_name)

    for col in cat:
        col_name = col.column_name
        unique_count = dataset[col_name].nunique()
        if unique_count and unique_count > 1:
            cat_for_corr.append(col_name)
    return num_for_corr, cat_for_corr


def _cramer_v(x: pd.Series, y: pd.Series) -> float:
    """Calculate Cramér's V: a measure of association between two nominal variables.
    Args:
        x: The array of observed values.
        y: The array of observed values.
    Returns:
        Value of the Cramér's V
    """
    arr = pd.crosstab(x, y).values
    chi2_stat = chi2_contingency(arr, correction=False)
    phi2 = chi2_stat[0] / arr.sum()
    n_rows, n_cols = arr.shape
    if min(n_cols - 1, n_rows - 1) == 0:
        value = np.nan
    else:
        value = np.sqrt(phi2 / min(n_cols - 1, n_rows - 1))

    return value


def get_pairwise_correlation(df, func: Callable[[pd.Series, pd.Series], float]) -> pd.DataFrame:
    """Compute pairwise correlation of columns
    Args:
        df: initial data frame.
        func: function for computing pairwise correlation.
    Returns:
        Correlation matrix.
    """
    columns = df.columns
    k = df.shape[1]
    if k <= 1:
        return pd.DataFrame()
    else:
        corr_array = np.eye(k)

        for i in range(k):
            for j in range(k):
                if i <= j:
                    continue
                c = func(df[columns[i]], df[columns[j]])
                corr_array[i, j] = c
                corr_array[j, i] = c
        return pd.DataFrame(data=corr_array, columns=columns, index=columns)


def _calculate_correlations(df: pd.DataFrame, num_for_corr, cat_for_corr, kind):
    """Calculate correlation matrix depending on the kind parameter
    Args:
        df: initial data frame.
        num_for_corr: list of feature names for pearson, spearman, and kendall correlation matrices.
        cat_for_corr: list of feature names for kramer_v correlation matrix.
        kind: Method of correlation:
            - pearson - standard correlation coefficient
            - kendall - Kendall Tau correlation coefficient
            - spearman - Spearman rank correlation
            - cramer_v - Cramer’s V measure of association
    Returns:
        Correlation matrix.
    """
    if kind == "pearson":
        return df[num_for_corr].corr("pearson")
    elif kind == "spearman":
        return df[num_for_corr].corr("spearman")
    elif kind == "kendall":
        return df[num_for_corr].corr("kendall")
    elif kind == "cramer_v":
        return get_pairwise_correlation(df[cat_for_corr], _cramer_v)


def calculate_correlations(
    dataset: pd.DataFrame, data_definition: DataDefinition, add_text_columns: Optional[list] = None
) -> Dict:
    num_for_corr, cat_for_corr = _select_features_for_corr(dataset, data_definition)
    if add_text_columns is not None:
        num_for_corr += add_text_columns
    correlations = {}

    for kind in ["pearson", "spearman", "kendall", "cramer_v"]:
        correlations[kind] = _calculate_correlations(dataset, num_for_corr, cat_for_corr, kind)

    return correlations


def calculate_cramer_v_correlation(column_name: str, dataset: pd.DataFrame, columns: List[str]) -> ColumnCorrelations:
    result_x = []
    result_y = []

    if not dataset[column_name].empty:
        for correlation_columns_name in columns:
            result_x.append(correlation_columns_name)
            result_y.append(_cramer_v(dataset[column_name], dataset[correlation_columns_name]))

    return ColumnCorrelations(
        column_name=column_name,
        kind="cramer_v",
        values=Distribution(x=result_x, y=result_y),
    )


def calculate_category_correlation(
    column_display_name: str,
    column: pd.Series,
    features: pd.DataFrame,
) -> List[ColumnCorrelations]:
    """For category columns calculate cramer_v correlation"""
    if column.empty or features.empty:
        return []

    result_x = []
    result_y = []

    for feature_name in features.columns:
        result_x.append(feature_name)
        result_y.append(_cramer_v(column, features[feature_name]))

    return [
        ColumnCorrelations(
            column_name=column_display_name,
            kind="cramer_v",
            values=Distribution(x=result_x, y=result_y),
        ),
    ]


def calculate_numerical_correlation(
    column_display_name: str,
    column: pd.Series,
    features: pd.DataFrame,
) -> List[ColumnCorrelations]:
    if column.empty or features.empty:
        return []

    result = []

    for kind in ["pearson", "spearman", "kendall"]:
        correlations_columns = []
        correlations_values = []

        for other_column_name in features.columns:
            correlations_columns.append(other_column_name)
            correlations_values.append(
                column.replace([np.inf, -np.inf], np.nan).corr(
                    features[other_column_name].replace([np.inf, -np.inf], np.nan), method=kind
                )
            )

        result.append(
            ColumnCorrelations(
                column_name=column_display_name,
                kind=kind,
                values=Distribution(x=correlations_columns, y=correlations_values),
            )
        )

    return result


def calculate_column_distribution(column: pd.Series, column_type: str) -> ColumnDistribution:
    if column.empty:
        distribution: ColumnDistribution = {}

    elif column_type == "num":
        # TODO: implement distribution for num column
        value_counts = column.value_counts(dropna=True)
        distribution = dict(value_counts)

    elif column_type == "cat":
        value_counts = column.value_counts(dropna=True)
        distribution = dict(value_counts)

    else:
        raise ValueError(f"Cannot calculate distribution for column type {column_type}")

    return distribution


def get_corr_method(method: Optional[str], target_correlation: Optional[str] = None, pearson_default: bool = True):
    if method is not None:
        return method
    if method is None and pearson_default is False:
        return target_correlation
    else:
        return "pearson"
