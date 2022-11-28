"""Methods and types for data drift calculations."""

from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence
from typing import Union

import numpy as np
import pandas as pd
from dataclasses import dataclass

from evidently.calculations.stattests import get_stattest
from evidently.options import DataDriftOptions
from evidently.utils.data_operations import DatasetColumns
from evidently.utils.data_operations import recognize_column_type
from evidently.utils.visualizations import Distribution
from evidently.utils.visualizations import get_distribution_for_column


@dataclass
class ColumnDataDriftMetrics:
    """One column drift metrics."""

    column_name: str
    column_type: str
    stattest_name: str
    drift_score: float
    drift_detected: bool
    threshold: float
    # distributions for the column
    current_distribution: Distribution
    reference_distribution: Distribution
    current_small_distribution: Optional[list] = None
    reference_small_distribution: Optional[list] = None
    # data for scatter plot for numeric features only
    current_scatter: Optional[Dict[str, list]] = None
    x_name: Optional[str] = None
    plot_shape: Optional[Dict[str, float]] = None
    # correlations for numeric features only
    current_correlations: Optional[Dict[str, float]] = None
    reference_correlations: Optional[Dict[str, float]] = None


@dataclass
class DatasetDrift:
    """Dataset drift calculation results"""

    number_of_drifted_columns: int
    dataset_drift_score: float
    dataset_drift: bool


@dataclass
class DatasetDriftMetrics:
    number_of_columns: int
    number_of_drifted_columns: int
    share_of_drifted_columns: float
    dataset_drift: bool
    drift_by_columns: Dict[str, ColumnDataDriftMetrics]
    options: DataDriftOptions
    dataset_columns: DatasetColumns


def get_one_column_drift(
    *,
    current_data: pd.DataFrame,
    reference_data: pd.DataFrame,
    column_name: str,
    options: DataDriftOptions,
    dataset_columns: DatasetColumns,
    column_type: Optional[str] = None,
) -> ColumnDataDriftMetrics:
    if column_name not in current_data:
        raise ValueError(f"Cannot find column '{column_name}' in current dataset")

    if column_name not in reference_data:
        raise ValueError(f"Cannot find column '{column_name}' in reference dataset")

    if column_type is None:
        column_type = recognize_column_type(dataset=reference_data, column_name=column_name, columns=dataset_columns)

    if column_type not in ("cat", "num"):
        raise ValueError(f"Cannot calculate drift metric for column '{column_name}' with type {column_type}")

    stattest = None

    if column_name == dataset_columns.utility_columns.target and column_type == "num":
        stattest = options.num_target_stattest_func

    elif column_name == dataset_columns.utility_columns.target and column_type == "cat":
        stattest = options.cat_target_stattest_func

    if not stattest:
        stattest = options.get_feature_stattest_func(column_name, column_type)

    threshold = options.get_threshold(column_name, column_type)
    current_column = current_data[column_name]
    reference_column = reference_data[column_name]

    # clean and check the column in reference dataset
    reference_column = reference_column.replace([-np.inf, np.inf], np.nan).dropna()

    if reference_column.empty:
        raise ValueError(
            f"An empty column '{column_name}' was provided for drift calculation in the reference dataset."
        )

    # clean and check the column in current dataset
    current_column = current_column.replace([-np.inf, np.inf], np.nan).dropna()

    if current_column.empty:
        raise ValueError(f"An empty column '{column_name}' was provided for drift calculation in the current dataset.")

    current_small_distribution = None
    reference_small_distribution = None
    current_correlations = None
    reference_correlations = None
    current_scatter = None
    x_name = None
    plot_shape = None

    if column_type == "num":
        if not pd.api.types.is_numeric_dtype(reference_column):
            raise ValueError(f"Column '{column_name}' in reference dataset should contain numerical values only.")

        if not pd.api.types.is_numeric_dtype(current_column):
            raise ValueError(f"Column '{column_name}' in current dataset should contain numerical values only.")

    drift_test_function = get_stattest(reference_column, current_column, column_type, stattest)
    drift_result = drift_test_function(reference_column, current_column, column_type, threshold)

    if column_type == "num":
        numeric_columns = dataset_columns.num_feature_names

        if column_name not in numeric_columns:
            # for target and prediction cases add the column_name in the numeric columns list
            numeric_columns = numeric_columns + [column_name]

        current_correlations = current_data[numeric_columns].corr()[column_name].to_dict()
        reference_correlations = reference_data[numeric_columns].corr()[column_name].to_dict()
        current_nbinsx = options.get_nbinsx(column_name)
        current_small_distribution = [
            t.tolist()
            for t in np.histogram(
                current_data[column_name][np.isfinite(current_data[column_name])],
                bins=current_nbinsx,
                density=True,
            )
        ]
        reference_small_distribution = [
            t.tolist()
            for t in np.histogram(
                reference_data[column_name][np.isfinite(reference_data[column_name])],
                bins=current_nbinsx,
                density=True,
            )
        ]
        current_scatter = {}
        current_scatter[column_name] = current_data[column_name]
        datetime_column_name = dataset_columns.utility_columns.date
        if datetime_column_name is not None:
            current_scatter["Timestamp"] = current_data[datetime_column_name]
            x_name = "Timestamp"
        else:
            current_scatter["Index"] = current_data.index
            x_name = "Index"

        plot_shape = {}
        reference_mean = reference_data[column_name].mean()
        reference_std = reference_data[column_name].std()
        plot_shape["y0"] = reference_mean - reference_std
        plot_shape["y1"] = reference_mean + reference_std

    elif column_type == "cat":
        reference_counts = reference_data[column_name].value_counts(sort=False)
        current_counts = current_data[column_name].value_counts(sort=False)
        keys = set(reference_counts.keys()).union(set(current_counts.keys()))

        for key in keys:
            if key not in reference_counts:
                reference_counts.loc[key] = 0
            if key not in current_counts:
                current_counts.loc[key] = 0

        reference_small_distribution = list(
            reversed(list(map(list, zip(*sorted(reference_counts.items(), key=lambda x: str(x[0]))))))
        )
        current_small_distribution = list(
            reversed(list(map(list, zip(*sorted(current_counts.items(), key=lambda x: str(x[0]))))))
        )

    current_distribution, reference_distribution = get_distribution_for_column(
        column_type=column_type,
        current=current_column,
        reference=reference_column,
    )
    if reference_distribution is None:
        raise ValueError(f"Cannot calculate reference distribution for column '{column_name}'.")

    return ColumnDataDriftMetrics(
        column_name=column_name,
        column_type=column_type,
        stattest_name=drift_test_function.display_name,
        drift_score=drift_result.drift_score,
        drift_detected=drift_result.drifted,
        threshold=drift_result.actual_threshold,
        current_distribution=current_distribution,
        reference_distribution=reference_distribution,
        current_small_distribution=current_small_distribution,
        reference_small_distribution=reference_small_distribution,
        current_correlations=current_correlations,
        reference_correlations=reference_correlations,
        current_scatter=current_scatter,
        x_name=x_name,
        plot_shape=plot_shape,
    )


def _get_pred_labels_from_prob(dataframe: pd.DataFrame, prediction_column: list) -> List[str]:
    """Get labels from probabilities from columns by prediction columns list"""
    array_prediction = dataframe[prediction_column].to_numpy()
    prediction_ids = np.argmax(array_prediction, axis=-1)
    prediction_labels = [prediction_column[x] for x in prediction_ids]
    return prediction_labels


def ensure_prediction_column_is_string(
    *,
    prediction_column: Optional[Union[str, Sequence]],
    current_data: pd.DataFrame,
    reference_data: pd.DataFrame,
    threshold: float = 0.5,
) -> Optional[str]:
    """Update dataset by predictions type:

    - if prediction column is None or a string, no dataset changes
    - (binary classification) if predictions is a list and its length equals 2
        set predicted_labels column by `threshold`
    - (multy label classification) if predictions is a list and its length is greater than 2
        set predicted_labels from probability values in columns by prediction column


    Returns:
         prediction column name.
    """
    result_prediction_column = None

    if prediction_column is None or isinstance(prediction_column, str):
        result_prediction_column = prediction_column

    elif isinstance(prediction_column, list):
        if len(prediction_column) > 2:
            reference_data["predicted_labels"] = _get_pred_labels_from_prob(reference_data, prediction_column)
            current_data["predicted_labels"] = _get_pred_labels_from_prob(current_data, prediction_column)
            result_prediction_column = "predicted_labels"

        elif len(prediction_column) == 2:
            reference_data["predicted_labels"] = (reference_data[prediction_column[0]] > threshold).astype(int)
            current_data["predicted_labels"] = (current_data[prediction_column[0]] > threshold).astype(int)
            result_prediction_column = "predicted_labels"

    return result_prediction_column


def get_dataset_drift(drift_metrics, drift_share=0.5) -> DatasetDrift:
    number_of_drifted_columns = sum([1 if drift.drift_detected else 0 for _, drift in drift_metrics.items()])
    share_drifted_columns = number_of_drifted_columns / len(drift_metrics)
    dataset_drift = bool(share_drifted_columns >= drift_share)
    return DatasetDrift(
        number_of_drifted_columns=number_of_drifted_columns,
        dataset_drift_score=share_drifted_columns,
        dataset_drift=dataset_drift,
    )


def _get_all_columns_for_drift(dataset_columns: DatasetColumns) -> List[str]:
    result = []
    target_column = dataset_columns.utility_columns.target

    if target_column:
        result.append(target_column)

    prediction_column = dataset_columns.utility_columns.prediction

    if isinstance(prediction_column, str):
        result.append(prediction_column)

    if dataset_columns.num_feature_names:
        result += dataset_columns.num_feature_names

    if dataset_columns.cat_feature_names:
        result += dataset_columns.cat_feature_names

    return result


def get_drift_for_columns(
    *,
    current_data: pd.DataFrame,
    reference_data: pd.DataFrame,
    dataset_columns: DatasetColumns,
    data_drift_options: DataDriftOptions,
    drift_share_threshold: Optional[float] = None,
    columns: Optional[List[str]] = None,
) -> DatasetDriftMetrics:
    if columns is None:
        # ensure prediction column is a string - add label values for classification tasks
        ensure_prediction_column_is_string(
            prediction_column=dataset_columns.utility_columns.prediction,
            current_data=current_data,
            reference_data=reference_data,
        )
        columns = _get_all_columns_for_drift(dataset_columns)

    drift_share_threshold = drift_share_threshold or data_drift_options.drift_share

    # calculate result
    drift_by_columns = {}

    for column_name in columns:
        drift_by_columns[column_name] = get_one_column_drift(
            current_data=current_data,
            reference_data=reference_data,
            column_name=column_name,
            options=data_drift_options,
            dataset_columns=dataset_columns,
        )

    dataset_drift = get_dataset_drift(drift_by_columns, drift_share_threshold)
    return DatasetDriftMetrics(
        number_of_columns=len(columns),
        number_of_drifted_columns=dataset_drift.number_of_drifted_columns,
        share_of_drifted_columns=dataset_drift.dataset_drift_score,
        dataset_drift=dataset_drift.dataset_drift,
        drift_by_columns=drift_by_columns,
        options=data_drift_options,
        dataset_columns=dataset_columns,
    )
