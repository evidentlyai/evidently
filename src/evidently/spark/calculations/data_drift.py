from typing import Optional
from typing import Union

import numpy as np
from pyspark.sql import functions as sf

from evidently.base_metric import ColumnName
from evidently.base_metric import DataDefinition
from evidently.calculations.data_drift import ColumnDataDriftMetrics
from evidently.calculations.data_drift import ColumnType
from evidently.calculations.data_drift import DistributionIncluded
from evidently.calculations.data_drift import DriftStatsField
from evidently.calculations.data_drift import ScatterField
from evidently.metric_results import ScatterAggField
from evidently.options.data_drift import DataDriftOptions
from evidently.spark import SparkEngine
from evidently.spark.base import SparkSeries
from evidently.spark.calculations.histogram import get_histogram
from evidently.spark.calculations.stattests.base import get_stattest
from evidently.spark.utils import calculate_stats
from evidently.spark.utils import is_numeric_column_dtype
from evidently.spark.visualizations import get_distribution_for_column
from evidently.spark.visualizations import get_text_data_for_plots
from evidently.spark.visualizations import prepare_df_for_time_index_plot


def get_one_column_drift(
    *,
    current_feature_data: SparkSeries,
    reference_feature_data: SparkSeries,
    # index_data: pd.Series,
    datetime_column: Optional[str],
    column: ColumnName,
    options: DataDriftOptions,
    data_definition: DataDefinition,
    column_type: ColumnType,
    agg_data: bool,
) -> ColumnDataDriftMetrics:
    if column_type not in (ColumnType.Numerical, ColumnType.Categorical, ColumnType.Text):
        raise ValueError(f"Cannot calculate drift metric for column '{column}' with type {column_type}")

    target = data_definition.get_target_column()
    stattest = None
    threshold = None
    if column.is_main_dataset():
        if target and column.name == target.column_name and column_type == ColumnType.Numerical:
            stattest = options.num_target_stattest_func

        elif target and column.name == target.column_name and column_type == ColumnType.Categorical:
            stattest = options.cat_target_stattest_func

        if not stattest:
            stattest = options.get_feature_stattest_func(column.name, column_type.value)

        threshold = options.get_threshold(column.name, column_type.value)
    current_column = current_feature_data
    reference_column = reference_feature_data

    # clean and check the column in reference dataset
    reference_column = reference_column.replace([-np.inf, np.inf], np.nan).dropna()

    if reference_column.rdd.isEmpty():
        raise ValueError(
            f"An empty column '{column.name}' was provided for drift calculation in the reference dataset."
        )

    # clean and check the column in current dataset
    current_column = current_column.replace([-np.inf, np.inf], np.nan).dropna()

    if current_column.rdd.isEmpty():
        raise ValueError(f"An empty column '{column.name}' was provided for drift calculation in the current dataset.")

    current_distribution = None
    reference_distribution = None
    current_small_distribution = None
    reference_small_distribution = None
    current_correlations = None
    reference_correlations = None

    typical_examples_cur = None
    typical_examples_ref = None
    typical_words_cur = None
    typical_words_ref = None

    if column_type == ColumnType.Numerical:
        if not is_numeric_column_dtype(reference_column, column):
            raise ValueError(f"Column '{column}' in reference dataset should contain numerical values only.")

        if not is_numeric_column_dtype(current_column, column):
            raise ValueError(f"Column '{column}' in current dataset should contain numerical values only.")

    drift_test_function = get_stattest(reference_column, current_column, column_type.value, stattest)
    drift_result = drift_test_function(
        reference_column,
        current_column,
        column_type,
        threshold,
        engine=SparkEngine,
        column_name=column.name,
    )

    scatter: Optional[Union[ScatterField, ScatterAggField]] = None
    if column_type == ColumnType.Numerical:
        current_nbinsx = options.get_nbinsx(column.name)
        current_small_distribution = get_histogram(current_column, column.name, current_nbinsx, density=True)
        reference_small_distribution = get_histogram(reference_column, column.name, current_nbinsx, density=True)
        if not agg_data:
            raise NotImplementedError("Spark Metrics only works with agg_data=True")

        current_scatter = {}

        df, prefix = prepare_df_for_time_index_plot(
            current_column,
            column.name,
            datetime_column,
        )
        current_scatter["current"] = df
        if prefix is None:
            x_name = "Index binned"
        else:
            x_name = f"Timestamp ({prefix})"

        plot_shape = {}
        reference_mean, reference_std = calculate_stats(reference_column, column.name, sf.mean, sf.stddev_pop)
        plot_shape["y0"] = reference_mean - reference_std
        plot_shape["y1"] = reference_mean + reference_std
        scatter = ScatterAggField(scatter=current_scatter, x_name=x_name, plot_shape=plot_shape)

    elif column_type == ColumnType.Categorical:
        pass  # todo: categorical
        # reference_counts = reference_column.value_counts(sort=False)
        # current_counts = current_column.value_counts(sort=False)
        # keys = set(reference_counts.keys()).union(set(current_counts.keys()))
        #
        # for key in keys:
        #     if key not in reference_counts:
        #         reference_counts.loc[key] = 0
        #     if key not in current_counts:
        #         current_counts.loc[key] = 0
        #
        # reference_small_distribution = np.array(
        #     reversed(
        #         list(
        #             map(
        #                 list,
        #                 zip(*sorted(reference_counts.items(), key=lambda x: str(x[0]))),
        #             )
        #         )
        #     )
        # )
        # current_small_distribution = np.array(
        #     reversed(
        #         list(
        #             map(
        #                 list,
        #                 zip(*sorted(current_counts.items(), key=lambda x: str(x[0]))),
        #             )
        #         )
        #     )
        # )
    if column_type != ColumnType.Text:
        # todo: categorical
        # prediction = data_definition.get_prediction_columns()
        # labels = data_definition.classification_labels()
        # predicted_values = prediction.predicted_values if prediction else None
        # if (
        #     column_type == ColumnType.Categorical
        #     and labels is not None
        #     and (
        #         (target and column.name == target.column_name)
        #         or (
        #             predicted_values
        #             and isinstance(predicted_values.column_name, str)
        #             and column.name == predicted_values.column_name
        #         )
        #     )
        # ):
        #     column_values = np.union1d(current_column.unique(), reference_column.unique())
        #     target_names = labels if isinstance(labels, list) else list(labels.values())
        #     new_values = np.setdiff1d(list(target_names), column_values)
        #     if len(new_values) > 0:
        #         raise ValueError(f"Values {new_values} not presented in 'target_names'")
        #     else:
        #         current_column = current_column.map(target_names)
        #         reference_column = reference_column.map(target_names)

        current_distribution, reference_distribution = get_distribution_for_column(
            column_type=column_type,
            column_name=column.name,
            current=current_column,
            reference=reference_column,
        )
        if reference_distribution is None:
            raise ValueError(f"Cannot calculate reference distribution for column '{column}'.")

    elif column_type == ColumnType.Text and drift_result.drifted:
        (
            typical_examples_cur,
            typical_examples_ref,
            typical_words_cur,
            typical_words_ref,
        ) = get_text_data_for_plots(reference_column, current_column)

    metrics = ColumnDataDriftMetrics(
        column_name=column.display_name,
        column_type=column_type.value,
        stattest_name=drift_test_function.display_name,
        drift_score=drift_result.drift_score,
        drift_detected=drift_result.drifted,
        stattest_threshold=drift_result.actual_threshold,
        current=DriftStatsField(
            distribution=current_distribution,
            small_distribution=DistributionIncluded(
                x=current_small_distribution[1].tolist(), y=current_small_distribution[0]
            )
            if current_small_distribution
            else None,
            correlations=current_correlations,
            characteristic_examples=typical_examples_cur,
            characteristic_words=typical_words_cur,
        ),
        reference=DriftStatsField(
            distribution=reference_distribution,
            small_distribution=DistributionIncluded(
                x=reference_small_distribution[1].tolist(), y=reference_small_distribution[0]
            )
            if reference_small_distribution
            else None,
            characteristic_examples=typical_examples_ref,
            characteristic_words=typical_words_ref,
            correlations=reference_correlations,
        ),
        scatter=scatter,
    )

    return metrics
