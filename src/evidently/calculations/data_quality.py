"""Methods for overall dataset quality calculations - rows count, a specific values count, etc."""

import dataclasses
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency

from evidently.metric_results import ColumnCorrelations
from evidently.metric_results import DatasetColumns
from evidently.metric_results import Distribution
from evidently.metric_results import Histogram
from evidently.metric_results import HistogramData
from evidently.utils.data_preprocessing import DataDefinition
from evidently.utils.types import ColumnDistribution
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


def get_features_stats(feature: pd.Series, feature_type: str) -> FeatureQualityStats:
    def get_percentage_from_all_values(value: Union[int, float]) -> float:
        return np.round(100 * value / all_values_count, 2)

    result = FeatureQualityStats(feature_type=feature_type)
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

    if feature_type == "num":
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

    if feature_type == "datetime":
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
        feature_name: get_features_stats(dataset[feature_name], feature_type="num")
        for feature_name in columns.num_feature_names
    }

    result.cat_features_stats = {
        feature_name: get_features_stats(dataset[feature_name], feature_type="cat")
        for feature_name in columns.cat_feature_names
    }

    if columns.utility_columns.date:
        date_list = columns.datetime_feature_names + [columns.utility_columns.date]

    else:
        date_list = columns.datetime_feature_names

    result.datetime_features_stats = {
        feature_name: get_features_stats(dataset[feature_name], feature_type="datetime") for feature_name in date_list
    }

    target_name = columns.utility_columns.target

    if target_name is not None and target_name in dataset:
        result.target_stats = {}

        if task == "classification":
            result.target_stats[target_name] = get_features_stats(dataset[target_name], feature_type="cat")

        else:
            result.target_stats[target_name] = get_features_stats(dataset[target_name], feature_type="num")

    prediction_name = columns.utility_columns.prediction

    if isinstance(prediction_name, str) and prediction_name in dataset:
        result.prediction_stats = {}

        if task == "classification":
            result.prediction_stats[prediction_name] = get_features_stats(dataset[prediction_name], feature_type="cat")

        else:
            result.prediction_stats[prediction_name] = get_features_stats(dataset[prediction_name], feature_type="num")

    return result


class DataQualityGetPlotData:
    def __init__(self) -> None:
        self.period_prefix: Optional[str] = None
        self.curr: Optional[pd.Series] = None
        self.ref: Optional[pd.Series] = None

    def calculate_main_plot(
        self,
        curr: pd.DataFrame,
        ref: Optional[pd.DataFrame],
        feature_name: str,
        feature_type: str,
        merge_small_cat: Optional[int] = MAX_CATEGORIES,
    ) -> Optional[Histogram]:
        if feature_type == "cat" and merge_small_cat is not None:
            if ref is not None:
                ref = ref.copy()
            if merge_small_cat is not None:
                curr, ref = self._transform_cat_data(curr.copy(), ref, feature_name, merge_small_cat)
        curr_data = curr[feature_name].dropna()
        ref_data = None
        if ref is not None:
            ref_data = ref[feature_name].dropna()

        if feature_type == "num":
            bins_for_hist: Histogram = make_hist_for_num_plot(curr_data, ref_data)
            log_ref_data = None
            if ref_data is not None:
                log_ref_data = np.log10(ref_data[ref_data > 0])
            bins_for_hist_log = make_hist_for_num_plot(
                np.log10(curr_data[curr_data > 0]),
                log_ref_data,
            )
            bins_for_hist.current_log = bins_for_hist_log.current
            bins_for_hist.reference_log = bins_for_hist_log.reference

            return bins_for_hist
        if feature_type == "cat":
            return make_hist_for_cat_plot(curr_data, ref_data, dropna=True)
        if feature_type == "datetime":
            freq = self._choose_agg_period(feature_name, ref, curr)
            curr_data = curr[feature_name].dt.to_period(freq=freq)
            curr_data = curr_data.value_counts().reset_index()
            curr_data.columns = [feature_name, "number_of_items"]
            curr_data[feature_name] = curr_data[feature_name].dt.to_timestamp()
            reference = None
            if ref is not None:
                ref_data = ref[feature_name].dt.to_period(freq=freq)
                ref_data = ref_data.value_counts().reset_index()
                ref_data.columns = [feature_name, "number_of_items"]
                ref_data[feature_name] = ref_data[feature_name].dt.to_timestamp()
                max_ref_date = ref_data[feature_name].max()
                min_curr_date = curr_data[feature_name].min()
                if max_ref_date == min_curr_date:
                    curr_data, ref_data = self._split_periods(curr_data, ref_data, feature_name)
                reference = ref_data
                reference.columns = ["x", "count"]
            curr_data.columns = ["x", "count"]
            return Histogram(current=HistogramData.from_df(curr_data), reference=HistogramData.from_df(reference))
        if feature_type == "text":
            return None

        raise ValueError(f"Unknown feature type {feature_type}")

    def calculate_data_in_time(
        self,
        curr: pd.DataFrame,
        ref: Optional[pd.DataFrame],
        feature_name: str,
        feature_type: str,
        datetime_name: str,
        merge_small_cat: Optional[int] = MAX_CATEGORIES,
    ):
        result = None
        if feature_type == "cat" and merge_small_cat is not None:
            if ref is not None:
                ref = ref.copy()
            curr, ref = self._transform_cat_data(curr.copy(), ref, feature_name, merge_small_cat)

        freq = self._choose_agg_period(datetime_name, ref, curr)
        df_for_time_plot_curr = (
            curr.assign(period=lambda x: x[datetime_name].dt.to_period(freq=freq))
            .loc[:, ["period", feature_name]]
            .copy()
        )
        df_for_time_plot_ref = None
        if ref is not None:
            df_for_time_plot_ref = (
                ref.assign(period=lambda x: x[datetime_name].dt.to_period(freq=freq))
                .loc[:, ["period", feature_name]]
                .copy()
            )
        if feature_type == "num":
            df_for_time_plot_curr = self._transform_df_to_time_mean_view(
                df_for_time_plot_curr,
                datetime_name,
                feature_name,
            )
            if df_for_time_plot_ref is not None:
                df_for_time_plot_ref = self._transform_df_to_time_mean_view(
                    df_for_time_plot_ref,
                    datetime_name,
                    feature_name,
                )
            result = {
                "current": df_for_time_plot_curr,
                "reference": df_for_time_plot_ref,
                "freq": self.period_prefix,
                "datetime_name": datetime_name,
            }

        if feature_type == "cat":
            df_for_time_plot_curr = self._transform_df_to_time_count_view(
                df_for_time_plot_curr,
                datetime_name,
                feature_name,
            )
            if df_for_time_plot_ref is not None:
                df_for_time_plot_ref = self._transform_df_to_time_count_view(
                    df_for_time_plot_ref,
                    datetime_name,
                    feature_name,
                )
            result = {
                "current": df_for_time_plot_curr,
                "reference": df_for_time_plot_ref,
                "freq": self.period_prefix,
                "datetime_name": datetime_name,
            }

        return result

    def calculate_data_by_target(
        self,
        curr: pd.DataFrame,
        ref: Optional[pd.DataFrame],
        feature_name: str,
        feature_type: str,
        target_name: str,
        target_type: str,
        merge_small_cat: Optional[int] = MAX_CATEGORIES,
    ):
        if feature_type == "cat" and target_type == "num":
            if ref is not None:
                ref = ref.copy()
            if merge_small_cat is not None:
                curr, ref = self._transform_cat_data(curr.copy(), ref, feature_name, merge_small_cat)
            return self._prepare_box_data(curr, ref, feature_name, target_name)
        if feature_type == "num" and target_type == "cat":
            if ref is not None:
                ref = ref.copy()
            if merge_small_cat is not None:
                curr, ref = self._transform_cat_data(curr.copy(), ref, target_name, merge_small_cat)
            return self._prepare_box_data(curr, ref, target_name, feature_name)
        if feature_type == "num" and target_type == "num":
            result = {}
            result["current"] = {
                feature_name: curr[feature_name].tolist(),
                target_name: curr[target_name].tolist(),
            }
            if ref is not None:
                result["reference"] = {
                    feature_name: ref[feature_name].tolist(),
                    target_name: ref[target_name].tolist(),
                }
            return result
        if feature_type == "cat" and target_type == "cat":
            if ref is not None:
                ref = ref.copy()
            if merge_small_cat is not None:
                curr, ref = self._transform_cat_data(curr.copy(), ref, feature_name, merge_small_cat)
            if ref is not None:
                ref = ref.copy()
            if merge_small_cat is not None:
                curr, ref = self._transform_cat_data(curr.copy(), ref, target_name, merge_small_cat, True)
            result = {}
            result["current"] = self._get_count_values(curr, target_name, feature_name)
            if ref is not None:
                result["reference"] = self._get_count_values(ref, target_name, feature_name)
            return result
        return None

    def _split_periods(self, curr_data, ref_data, feature_name):
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

    def _get_count_values(self, df: pd.DataFrame, target_column: str, feature_name: Optional[str]):
        df = df.groupby([target_column, feature_name]).size()
        df.name = "count_objects"
        df = df.reset_index()
        return df[df["count_objects"] > 0]

    def _prepare_box_data(
        self, curr: pd.DataFrame, ref: Optional[pd.DataFrame], cat_feature_name: str, num_feature_name: str
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

    def _transform_cat_data(
        self,
        curr: pd.DataFrame,
        ref: Optional[pd.DataFrame],
        feature_name: str,
        merge_small_cat: int,
        rewrite: bool = False,
    ) -> Tuple[pd.DataFrame, Optional[pd.DataFrame]]:
        if self.curr is not None and rewrite is not True:
            return self.curr, self.ref
        if ref is not None:
            unique_values = len(
                np.union1d(
                    curr[feature_name].astype(str).unique(),
                    ref[feature_name].astype(str).unique(),
                )
            )
        else:
            unique_values = curr[feature_name].astype(str).nunique()

        if unique_values > merge_small_cat:
            curr_cats = curr[feature_name].astype(str).value_counts(normalize=True)

            if ref is not None:
                ref_cats = ref[feature_name].astype(str).value_counts(normalize=True)
                categories = pd.concat([curr_cats, ref_cats])

            else:
                categories = curr_cats

            cats = categories.sort_values(ascending=False).index.drop_duplicates(keep="first")[:merge_small_cat].values

            curr[feature_name] = curr[feature_name].apply(lambda x: x if str(x) in cats else "other")
            if ref is not None:
                ref[feature_name] = ref[feature_name].apply(lambda x: x if str(x) in cats else "other")
            self.curr = curr
            self.ref = ref
        return curr, ref

    def _choose_agg_period(
        self, date_column: str, reference_data: Optional[pd.DataFrame], current_data: pd.DataFrame
    ) -> str:
        optimal_points = 150
        prefix_dict = {
            "A": "year",
            "Q": "quarter",
            "M": "month",
            "W": "week",
            "D": "day",
            "H": "hour",
        }
        datetime_feature = current_data[date_column]
        if reference_data is not None:
            datetime_feature = datetime_feature.append(reference_data[date_column])
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
        self.period_prefix = prefix_dict[time_points.idxmin()]
        return str(time_points.idxmin())

    def _transform_df_to_time_mean_view(self, df: pd.DataFrame, date_column: str, feature_name: str):
        df = df.groupby("period")[feature_name].mean().reset_index()
        df[date_column] = df["period"].dt.to_timestamp()
        return df

    def _transform_df_to_time_count_view(self, df: pd.DataFrame, date_column: str, feature_name: str):
        df = df.groupby(["period", feature_name]).size()
        df.name = "num"
        df = df.reset_index()
        df[date_column] = df["period"].dt.to_timestamp()
        return df[df["num"] > 0]


def _select_features_for_corr(dataset: pd.DataFrame, data_definition: DataDefinition) -> tuple:
    """Define which features should be used for calculating correlation matrices:
        - for pearson, spearman, and kendall correlation matrices we select numerical features which have > 1
            unique values;
        - for kramer_v correlation matrix, we select categorical features which have > 1 unique values.
    Args:
        columns: all columns data information.
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


def calculate_category_column_correlations(
    column_name: str, dataset: pd.DataFrame, columns: List[str]
) -> Dict[str, ColumnCorrelations]:
    """For category columns calculate cramer_v correlation"""
    if dataset[column_name].empty:
        return {}

    if not columns:
        return {}

    correlation = calculate_cramer_v_correlation(column_name, dataset, columns)

    if pd.isnull(correlation.values.y).all():
        return {}

    else:
        return {correlation.kind: correlation}


def calculate_numerical_column_correlations(
    column_name: str, dataset: pd.DataFrame, columns: List[str]
) -> Dict[str, ColumnCorrelations]:
    if dataset[column_name].empty or not columns:
        return {}

    if not columns:
        return {}

    result: Dict[str, ColumnCorrelations] = {}
    column = dataset[column_name]

    for kind in ["pearson", "spearman", "kendall"]:
        correlations_columns = []
        correlations_values = []

        for other_column_name in columns:
            correlations_columns.append(other_column_name)
            correlations_values.append(column.corr(dataset[other_column_name], method=kind))

        result[kind] = ColumnCorrelations(
            column_name=column_name,
            kind=kind,
            values=Distribution(x=correlations_columns, y=correlations_values),
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
