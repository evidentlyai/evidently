from dataclasses import dataclass
from typing import Dict
from typing import Optional

import pandas as pd
import numpy as np

from evidently import ColumnMapping
from evidently.analyzers.data_quality_analyzer import DataQualityStats
from evidently.analyzers.data_quality_analyzer import DataQualityAnalyzer
from evidently.analyzers.utils import recognize_task
from evidently.options.quality_metrics import QualityMetricsOptions
from evidently.options import OptionsProvider
from evidently.v2.metrics.base_metric import InputData
from evidently.v2.metrics.base_metric import Metric
from evidently.v2.metrics.utils import make_hist_for_num_plot
from evidently.v2.metrics.utils import make_hist_for_cat_plot


@dataclass
class DataQualityMetricsResults:
    features_stats: DataQualityStats
    distr_for_plots: Dict[str, Dict[str, pd.DataFrame]]
    counts_of_values: Dict[str, Dict[str, pd.DataFrame]]
    correlations: Dict[str, pd.DataFrame] = None
    reference_features_stats: Optional[DataQualityStats] = None


class DataQualityMetrics(Metric[DataQualityMetricsResults]):
    def __init__(self, options: QualityMetricsOptions = None) -> None:
        self.analyzer = DataQualityAnalyzer()
        self.analyzer.options_provider = OptionsProvider()

        if options is not None:
            self.analyzer.options_provider.add(options)

    def calculate(self, data: InputData, metrics: dict) -> DataQualityMetricsResults:
        if data.current_data is None:
            raise ValueError("Current dataset should be present")

        if data.reference_data is None:
            analyzer_results = self.analyzer.calculate(
                reference_data=data.current_data, current_data=None, column_mapping=data.column_mapping
            )
            features_stats = analyzer_results.reference_features_stats
            correlations = analyzer_results.reference_correlations
            reference_features_stats = None

        else:
            analyzer_results = self.analyzer.calculate(
                reference_data=data.reference_data, current_data=data.current_data, column_mapping=data.column_mapping
            )
            features_stats = analyzer_results.current_features_stats
            correlations = analyzer_results.current_correlations
            reference_features_stats = analyzer_results.reference_features_stats

        # data for visualisation
        if data.reference_data is not None:
            reference_data = data.reference_data

        else:
            reference_data = None

        distr_for_plots = {}
        counts_of_values = {}

        if data.column_mapping.task is not None:
            task = data.column_mapping.task

        elif data.column_mapping.task is None and analyzer_results.columns.utility_columns.target:
            if reference_data is None:
                data_for_task_detection = data.current_data

            else:
                data_for_task_detection = reference_data

            task = recognize_task(analyzer_results.columns.utility_columns.target, data_for_task_detection)

        else:
            task = None

        target_prediction_columns = [
            t
            for t in [
                analyzer_results.columns.utility_columns.target,
                analyzer_results.columns.utility_columns.prediction,
            ]
            if t is not None
        ]
        num_columns = analyzer_results.columns.num_feature_names
        cat_columns = analyzer_results.columns.cat_feature_names
        if task == ColumnMapping.REGRESSION_TASK:
            num_columns.extend(target_prediction_columns)
        if task == ColumnMapping.CLASSIFICATION_TASK:
            cat_columns.extend(target_prediction_columns)

        for feature in num_columns:
            counts_of_value_feature = {}
            curr_feature = data.current_data[feature]
            current_counts = data.current_data[feature].value_counts(dropna=False).reset_index()
            current_counts.columns = ["x", "count"]
            counts_of_value_feature["current"] = current_counts

            ref_feature = None

            if reference_data is not None:
                ref_feature = reference_data[feature]

                reference_counts = ref_feature.value_counts(dropna=False).reset_index()
                reference_counts.columns = ["x", "count"]
                counts_of_value_feature["reference"] = reference_counts

            counts_of_values[feature] = counts_of_value_feature
            distr_for_plots[feature] = make_hist_for_num_plot(curr_feature, ref_feature)

        for feature in cat_columns:
            curr_feature = data.current_data[feature]
            ref_feature = None
            if reference_data is not None:
                ref_feature = reference_data[feature]
            counts_of_values[feature] = make_hist_for_cat_plot(curr_feature, ref_feature)
            distr_for_plots[feature] = counts_of_values[feature]

        return DataQualityMetricsResults(
            features_stats=features_stats,
            distr_for_plots=distr_for_plots,
            counts_of_values=counts_of_values,
            correlations=correlations,
            reference_features_stats=reference_features_stats,
        )


@dataclass
class DataQualityStabilityMetricsResults:
    number_not_stable_target: Optional[int] = None
    number_not_stable_prediction: Optional[int] = None


class DataQualityStabilityMetrics(Metric[DataQualityStabilityMetricsResults]):
    """Calculates stability by target and prediction"""

    def calculate(self, data: InputData, metrics: dict) -> DataQualityStabilityMetricsResults:
        result = DataQualityStabilityMetricsResults()
        target_name = data.column_mapping.target
        prediction_name = data.column_mapping.prediction
        columns = [column for column in data.current_data.columns if column not in (target_name, prediction_name)]
        duplicates = data.current_data[data.current_data.duplicated(subset=columns, keep=False)]

        if target_name in data.current_data:
            result.number_not_stable_target = duplicates.drop(
                data.current_data[data.current_data.duplicated(subset=columns + [target_name], keep=False)].index
            ).shape[0]

        if prediction_name in data.current_data:
            result.number_not_stable_prediction = duplicates.drop(
                data.current_data[data.current_data.duplicated(subset=columns + [prediction_name], keep=False)].index
            ).shape[0]

        return result


@dataclass
class DataQualityValueListMetricsResults:
    number_in_list: int
    number_not_in_list: int
    share_in_list: float
    share_not_in_list: float
    counts_of_value: Dict[str, pd.DataFrame]


class DataQualityValueListMetrics(Metric[DataQualityValueListMetricsResults]):
    """Calculates count and shares of values in the predefined values list"""

    column: str
    values: Optional[list]

    def __init__(self, column: str, values: Optional[list] = None) -> None:
        self.values = values
        self.column = column

    def calculate(self, data: InputData, metrics: dict) -> DataQualityValueListMetricsResults:
        if self.values is None:
            if data.reference_data is None:
                raise ValueError("Reference or values list should be present")
            self.values = data.reference_data[self.column].unique()

        rows_count = data.current_data.shape[0]
        values_in_list = data.current_data[self.column].isin(self.values).sum()
        number_not_in_list = rows_count - values_in_list
        counts_of_value = {}
        current_counts = data.current_data[self.column].value_counts(dropna=False).reset_index()
        current_counts.columns = ["x", "count"]
        counts_of_value["current"] = current_counts
        if data.reference_data is not None:
            reference_counts = data.reference_data[self.column].value_counts(dropna=False).reset_index()
            reference_counts.columns = ["x", "count"]
            counts_of_value["reference"] = reference_counts

        return DataQualityValueListMetricsResults(
            number_in_list=values_in_list,
            number_not_in_list=rows_count - values_in_list,
            share_in_list=values_in_list / rows_count,
            share_not_in_list=number_not_in_list / rows_count,
            counts_of_value=counts_of_value,
        )


@dataclass
class DataQualityValueRangeMetricsResults:
    number_in_range: int
    number_not_in_range: int
    share_in_range: float
    share_not_in_range: float
    distr_for_plot: Dict[str, pd.DataFrame]


class DataQualityValueRangeMetrics(Metric[DataQualityValueRangeMetricsResults]):
    """Calculates count and shares of values in the predefined values range"""

    column: str
    left: Optional[float]
    right: Optional[float]

    def __init__(self, column: str, left: Optional[float] = None, right: Optional[float] = None) -> None:
        self.left = left
        self.right = right
        self.column = column

    def calculate(self, data: InputData, metrics: dict) -> DataQualityValueRangeMetricsResults:
        if (self.left is None or self.right is None) and data.reference_data is None:
            raise ValueError("Reference should be present")

        if self.left is None:
            self.left = data.reference_data[self.column].min()

        if self.right is None:
            self.right = data.reference_data[self.column].max()

        rows_count = data.current_data[self.column].dropna().shape[0]
        number_in_range = (
            data.current_data[self.column]
            .dropna()
            .between(left=float(self.left), right=float(self.right), inclusive="both")
            .sum()
        )
        number_not_in_range = rows_count - number_in_range

        # visualisation
        curr_feature = data.current_data[self.column]

        ref_feature = None
        if data.reference_data is not None:
            ref_feature = data.reference_data[self.column]

        distr_for_plot = make_hist_for_num_plot(curr_feature, ref_feature)

        return DataQualityValueRangeMetricsResults(
            number_in_range=number_in_range,
            number_not_in_range=number_not_in_range,
            share_in_range=number_in_range / rows_count,
            share_not_in_range=number_not_in_range / rows_count,
            distr_for_plot=distr_for_plot,
        )


@dataclass
class DataQualityValueQuantileMetricsResults:
    # calculated value of the quantile
    value: float
    # range of the quantile (from 0 to 1)
    quantile: float
    distr_for_plot: Dict[str, pd.DataFrame]


class DataQualityValueQuantileMetrics(Metric[DataQualityValueQuantileMetricsResults]):
    """Calculates quantile with specified range"""

    column: str
    quantile: float

    def __init__(self, column: str, quantile: float) -> None:
        if quantile is not None:
            if not 0 <= quantile <= 1:
                raise ValueError("Quantile should all be in the interval [0, 1].")

        self.column = column
        self.quantile = quantile

    def calculate(self, data: InputData, metrics: dict) -> DataQualityValueQuantileMetricsResults:
        # visualisation

        curr_feature = data.current_data[self.column]

        ref_feature = None
        if data.reference_data is not None:
            ref_feature = data.reference_data[self.column]

        distr_for_plot = make_hist_for_num_plot(curr_feature, ref_feature)
        return DataQualityValueQuantileMetricsResults(
            value=data.current_data[self.column].quantile(self.quantile),
            quantile=self.quantile,
            distr_for_plot=distr_for_plot,
        )


@dataclass
class DataQualityCorrelationMetricsResults:
    current_correlation_matrix: pd.DataFrame
    num_features: list
    target_prediction_correlation: Optional[float]
    abs_max_target_features_correlation: Optional[float]
    abs_max_prediction_features_correlation: Optional[float]
    abs_max_correlation: Optional[float]
    abs_max_num_features_correlation: Optional[float]
    reference_target_prediction_correlation: Optional[float]
    reference_abs_max_target_features_correlation: Optional[float]
    reference_abs_max_prediction_features_correlation: Optional[float]
    reference_abs_max_correlation: Optional[float]
    reference_abs_max_num_features_correlation: Optional[float]
    reference_correlation_matrix: pd.DataFrame = None


class DataQualityCorrelationMetrics(Metric[DataQualityCorrelationMetricsResults]):
    """Calculate different correlations with target, predictions and features"""

    method: str

    def __init__(self, method: str = "pearson") -> None:
        self.method = method

    def calculate(self, data: InputData, metrics: dict) -> DataQualityCorrelationMetricsResults:
        target_name = data.column_mapping.target
        prediction_name = data.column_mapping.prediction
        num_features = data.column_mapping.numerical_features

        if not target_name:
            raise ValueError("Target should be present")

        if not data.column_mapping.prediction:
            raise ValueError("Prediction should be present")

        if target_name not in data.current_data:
            raise ValueError("Target column should be present in current data")

        if data.column_mapping.prediction not in data.current_data:
            raise ValueError("Prediction column should be present in current data")

        reference_correlations = None
        reference_correlations_for_plot = None
        current_correlations = data.current_data.corr(method=self.method)
        current_correlations_for_plot = current_correlations.copy()

        if data.reference_data is not None:
            reference_correlations = data.reference_data.corr(method=self.method)
            reference_correlations_for_plot = reference_correlations.copy()
            np.fill_diagonal(reference_correlations.values, 0)

        if num_features is None:
            num_features = [i for i in current_correlations if i not in [target_name, prediction_name]]

        # we will get 1 for all column/column correlation in the diagonal, fill it with 0
        np.fill_diagonal(current_correlations.values, 0)

        if reference_correlations is not None:
            np.fill_diagonal(reference_correlations.values, 0)

        target_prediction_correlation = current_correlations.loc[prediction_name, target_name]

        if reference_correlations is not None:
            reference_target_prediction_correlation = reference_correlations.loc[prediction_name, target_name]
        else:
            reference_target_prediction_correlation = None

        abs_max_target_features_correlation = current_correlations.loc[target_name, num_features].abs().max()

        if reference_correlations is not None:
            reference_abs_max_target_features_correlation = (
                current_correlations.loc[target_name, num_features].abs().max()
            )

        else:
            reference_abs_max_target_features_correlation = None

        abs_max_prediction_features_correlation = current_correlations.loc[prediction_name, num_features].abs().max()

        if reference_correlations is not None:
            reference_abs_max_prediction_features_correlation = (
                current_correlations.loc[prediction_name, num_features].abs().max()
            )

        else:
            reference_abs_max_prediction_features_correlation = None

        if data.column_mapping.is_classification_task() is not None:
            corr_features = num_features

        else:
            corr_features = num_features + [target_name, prediction_name]

        abs_max_correlation = current_correlations.loc[corr_features, corr_features].abs().max().max()

        if reference_correlations is not None:
            reference_abs_max_correlation = reference_correlations.loc[corr_features, corr_features].abs().max().max()

        else:
            reference_abs_max_correlation = None

        abs_max_num_features_correlation = current_correlations.loc[num_features, num_features].abs().max().max()

        if reference_correlations is not None:
            reference_abs_max_num_features_correlation = (
                reference_correlations.loc[num_features, num_features].abs().max().max()
            )

        else:
            reference_abs_max_num_features_correlation = None

        return DataQualityCorrelationMetricsResults(
            current_correlation_matrix=current_correlations_for_plot,
            num_features=num_features,
            target_prediction_correlation=target_prediction_correlation,
            abs_max_target_features_correlation=abs_max_target_features_correlation,
            abs_max_prediction_features_correlation=abs_max_prediction_features_correlation,
            abs_max_correlation=abs_max_correlation,
            abs_max_num_features_correlation=abs_max_num_features_correlation,
            reference_target_prediction_correlation=reference_target_prediction_correlation,
            reference_abs_max_target_features_correlation=reference_abs_max_target_features_correlation,
            reference_abs_max_prediction_features_correlation=reference_abs_max_prediction_features_correlation,
            reference_abs_max_correlation=reference_abs_max_correlation,
            reference_abs_max_num_features_correlation=reference_abs_max_num_features_correlation,
            reference_correlation_matrix=reference_correlations_for_plot,
        )
