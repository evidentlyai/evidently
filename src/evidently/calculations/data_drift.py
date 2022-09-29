"""Methods and types for data drift calculations"""

from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Union

import numpy as np
import pandas as pd
from dataclasses import dataclass

from evidently.calculations.stattests import PossibleStatTestType
from evidently.calculations.stattests import get_stattest
from evidently.options import DataDriftOptions
from evidently.utils.data_operations import DatasetColumns
from evidently.utils.data_operations import recognize_column_type
from evidently.utils.data_operations import recognize_task
from evidently.utils.visualizations import get_distribution_for_column


@dataclass
class ColumnDataDriftMetrics:
    """One column drift metrics"""

    column_name: str
    column_type: str
    stattest_name: str
    drift_score: float
    drift_detected: bool
    threshold: float
    # distributions for the column
    current_distribution: Optional[pd.DataFrame] = None
    reference_distribution: Optional[pd.DataFrame] = None
    current_small_distribution: Optional[list] = None
    reference_small_distribution: Optional[list] = None
    # correlations for numeric features only
    current_correlations: Optional[Dict[str, float]] = None
    reference_correlations: Optional[Dict[str, float]] = None


@dataclass
class DatasetDriftMetrics:
    n_features: int
    n_drifted_features: int
    share_drifted_features: float
    dataset_drift: bool
    drift_by_columns: Dict[str, ColumnDataDriftMetrics]
    options: DataDriftOptions
    columns: DatasetColumns


def get_one_column_drift(
    *,
    current_data: pd.DataFrame,
    reference_data: pd.DataFrame,
    column_name: str,
    options: DataDriftOptions,
    dataset_columns: DatasetColumns,
    column_type: Optional[str] = None,
) -> ColumnDataDriftMetrics:

    if column_type is None:
        column_type = recognize_column_type(column_name, dataset_columns)

    if column_type not in ("cat", "num"):
        raise ValueError(f"Cannot calculate drift metric for column {column_name} with type {column_type}")

    if column_name == dataset_columns.utility_columns.target and column_type == "num":
        stattest = options.num_target_stattest_func

    elif column_name == dataset_columns.utility_columns.target and column_type == "cat":
        stattest = options.cat_target_stattest_func

    else:
        stattest = options.get_feature_stattest_func(column_name, column_type)

    threshold = options.get_threshold(column_name)
    current_column = current_data[column_name]
    reference_column = reference_data[column_name]

    if column_type == "num":
        if not pd.api.types.is_numeric_dtype(reference_column):
            raise ValueError(f"Column {column_name} in reference dataset should contain numerical values only.")

        if not pd.api.types.is_numeric_dtype(current_column):
            raise ValueError(f"Column {column_name} in current dataset should contain numerical values only.")

    reference_column = reference_column.replace([-np.inf, np.inf], np.nan).dropna()

    if reference_column.empty:
        raise ValueError(f"Column '{column_name}' in reference dataset has no values for drift calculation.")

    current_column = current_column.replace([-np.inf, np.inf], np.nan).dropna()

    if current_column.empty:
        raise ValueError(f"Column '{column_name}' in current dataset has no values for drift calculation.")

    drift_test_function = get_stattest(reference_column, current_column, column_type, stattest)
    drift_result = drift_test_function(reference_column, current_column, column_type, threshold)
    result = ColumnDataDriftMetrics(
        column_name=column_name,
        column_type=column_type,
        stattest_name=drift_test_function.display_name,
        drift_score=drift_result.drift_score,
        drift_detected=drift_result.drifted,
        threshold=drift_result.actual_threshold,
    )

    if column_type == "num":
        if not pd.api.types.is_numeric_dtype(reference_column) or not pd.api.types.is_numeric_dtype(current_column):
            raise ValueError(f"Column {column_name} should only contain numerical values.")
        numeric_columns = dataset_columns.num_feature_names
        result.current_correlations = current_data[numeric_columns + [column_name]].corr()[column_name].to_dict()
        result.reference_correlations = reference_data[numeric_columns + [column_name]].corr()[column_name].to_dict()

    distribution_for_plot = get_distribution_for_column(
        column_name=column_name,
        column_type=column_type,
        current=current_column,
        reference=reference_column,
    )
    result.current_distribution = distribution_for_plot["current"]
    result.reference_distribution = distribution_for_plot["reference"]
    return result


def _get_pred_labels_from_prob(dataframe: pd.DataFrame, prediction_column: list) -> List[str]:
    """Get labels from probabilities from columns by prediction columns list"""
    array_prediction = dataframe[prediction_column].to_numpy()
    prediction_ids = np.argmax(array_prediction, axis=-1)
    prediction_labels = [prediction_column[x] for x in prediction_ids]
    return prediction_labels


def define_predictions_type(
    *,
    prediction_column: Optional[Union[str, Sequence]],
    current_data: pd.DataFrame,
    reference_data: pd.DataFrame,
    threshold: float,
) -> Optional[str]:
    """
    Update dataset by predictions type:
    - if prediction column is None or a string, no dataset changes
    - (binary classification) if predictions is a list and its length equals 2
        set predicted_labels column by `classification_threshold`
    - (multy label classification) if predictions is a list and its length is greater than 2
        set predicted_labels from probability values in columns by prediction column

    Returns prediction column name.
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


def get_dataset_drift(drift_metrics, drift_share=0.5) -> Tuple[int, float, bool]:
    n_drifted_features = sum([1 if drift.drift_detected else 0 for _, drift in drift_metrics.items()])
    share_drifted_features = n_drifted_features / len(drift_metrics)
    dataset_drift = bool(share_drifted_features >= drift_share)
    return n_drifted_features, share_drifted_features, dataset_drift


def get_drift_for_columns(
    *,
    current_data: pd.DataFrame,
    reference_data: pd.DataFrame,
    dataset_columns: DatasetColumns,
    data_drift_options: DataDriftOptions,
    drift_share_threshold: Optional[float] = None,
    columns: Optional[List[str]] = None,
) -> DatasetDriftMetrics:
    num_feature_names = dataset_columns.num_feature_names
    cat_feature_names = dataset_columns.cat_feature_names
    target_column = dataset_columns.utility_columns.target
    prediction_column = dataset_columns.utility_columns.prediction
    drift_share = drift_share_threshold or data_drift_options.drift_share
    # define type of target and prediction
    if target_column is not None:
        task = recognize_task(target_column, reference_data)
        if task == "regression":
            num_feature_names += [target_column]
        else:
            cat_feature_names += [target_column]

    if prediction_column is not None:
        if isinstance(prediction_column, list) and len(prediction_column) > 2:
            reference_data["predicted_labels"] = _get_pred_labels_from_prob(reference_data, prediction_column)
            current_data["predicted_labels"] = _get_pred_labels_from_prob(current_data, prediction_column)
            dataset_columns.utility_columns.prediction = "predicted_labels"
            cat_feature_names += [dataset_columns.utility_columns.prediction]

        elif isinstance(prediction_column, list) and len(prediction_column) == 2:
            reference_data["prediction"] = reference_data[prediction_column[0]].values
            current_data["prediction"] = current_data[prediction_column[0]].values
            dataset_columns.utility_columns.prediction = "prediction"
            num_feature_names += [dataset_columns.utility_columns.prediction]

        elif isinstance(prediction_column, str):
            if (
                pd.api.types.is_numeric_dtype(reference_data[prediction_column].dtype)
                and reference_data[prediction_column].nunique() > 5
            ):
                num_feature_names += [prediction_column]
            else:
                cat_feature_names += [prediction_column]

    # calculate result
    drift_by_columns = {}

    for feature_name in num_feature_names:
        feature_type = "num"
        drift_result = get_one_column_drift(
            current_data=current_data,
            reference_data=reference_data,
            column_name=feature_name,
            options=data_drift_options,
            dataset_columns=dataset_columns,
            column_type=feature_type,
        )

        current_nbinsx = data_drift_options.get_nbinsx(feature_name)
        drift_by_columns[feature_name] = ColumnDataDriftMetrics(
            column_name=feature_name,
            column_type=feature_type,
            stattest_name=drift_result.stattest_name,
            drift_score=drift_result.drift_score,
            drift_detected=drift_result.drift_detected,
            threshold=drift_result.threshold,
            current_distribution=drift_result.current_distribution,
            reference_distribution=drift_result.reference_distribution,
            current_small_distribution=[
                t.tolist()
                for t in np.histogram(
                    current_data[feature_name][np.isfinite(current_data[feature_name])],
                    bins=current_nbinsx,
                    density=True,
                )
            ],
            reference_small_distribution=[
                t.tolist()
                for t in np.histogram(
                    reference_data[feature_name][np.isfinite(reference_data[feature_name])],
                    bins=current_nbinsx,
                    density=True,
                )
            ],
        )

    for feature_name in cat_feature_names:
        feature_ref_data = reference_data[feature_name].dropna()
        feature_cur_data = current_data[feature_name].dropna()

        feature_type = "cat"
        drift_result = get_one_column_drift(
            current_data=current_data,
            reference_data=reference_data,
            column_name=feature_name,
            options=data_drift_options,
            dataset_columns=dataset_columns,
            column_type=feature_type,
        )
        ref_counts = feature_ref_data.value_counts(sort=False)
        cur_counts = feature_cur_data.value_counts(sort=False)
        keys = set(ref_counts.keys()).union(set(cur_counts.keys()))

        for key in keys:
            if key not in ref_counts:
                ref_counts.loc[key] = 0
            if key not in cur_counts:
                cur_counts.loc[key] = 0

        ref_small_hist = list(reversed(list(map(list, zip(*sorted(ref_counts.items(), key=lambda x: str(x[0])))))))
        cur_small_hist = list(reversed(list(map(list, zip(*sorted(cur_counts.items(), key=lambda x: str(x[0])))))))
        drift_by_columns[feature_name] = ColumnDataDriftMetrics(
            reference_small_distribution=ref_small_hist,
            current_small_distribution=cur_small_hist,
            current_distribution=drift_result.current_distribution,
            reference_distribution=drift_result.reference_distribution,
            column_name=feature_name,
            column_type=feature_type,
            stattest_name=drift_result.stattest_name,
            drift_score=drift_result.drift_score,
            drift_detected=drift_result.drift_detected,
            threshold=drift_result.threshold,
        )

    n_drifted_features, share_drifted_features, dataset_drift = get_dataset_drift(drift_by_columns, drift_share)
    return DatasetDriftMetrics(
        n_features=len(num_feature_names) + len(cat_feature_names),
        n_drifted_features=n_drifted_features,
        share_drifted_features=share_drifted_features,
        dataset_drift=dataset_drift,
        drift_by_columns=drift_by_columns,
        options=data_drift_options,
        columns=dataset_columns,
    )
