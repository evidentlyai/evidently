"""Methods for data drift calculations"""

import collections
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
from evidently.utils.data_operations import process_columns
from evidently.utils.data_operations import recognize_task
from evidently.utils.visualizations import get_distribution_for_column

PValueWithDrift = collections.namedtuple("PValueWithDrift", ["p_value", "drifted"])


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


@dataclass
class DataDriftMetrics:
    """Class for drift values"""

    column_name: str
    stattest_name: str
    drift_score: float
    drift_detected: bool
    threshold: float
    # correlations for numeric features
    reference_correlations: Optional[Dict[str, float]] = None
    current_correlations: Optional[Dict[str, float]] = None


def calculate_data_drift(
    *,
    current_column: pd.Series,
    reference_column: pd.Series,
    column_name: str,
    stattest: Optional[PossibleStatTestType],
    threshold: Optional[float],
    column_type: str,
) -> DataDriftMetrics:
    reference_column = reference_column.replace([-np.inf, np.inf], np.nan).dropna()

    if reference_column.empty:
        raise ValueError(f"Column '{column_name}' in reference dataset has no values for drift calculation.")

    current_column = current_column.replace([-np.inf, np.inf], np.nan).dropna()

    if current_column.empty:
        raise ValueError(f"Column '{column_name}' in current dataset has no values for drift calculation.")

    drift_test_function = get_stattest(reference_column, current_column, column_type, stattest)
    drift_result = drift_test_function(reference_column, current_column, column_type, threshold)
    return DataDriftMetrics(
        column_name=column_name,
        stattest_name=drift_test_function.display_name,
        drift_score=drift_result.drift_score,
        drift_detected=drift_result.drifted,
        threshold=drift_result.actual_threshold,
    )


def calculate_data_drift_for_category_feature(
    *,
    current_column: pd.Series,
    reference_column: pd.Series,
    column_name: str,
    stattest: Optional[PossibleStatTestType],
    threshold: Optional[float],
):
    return calculate_data_drift(
        current_column=current_column,
        reference_column=reference_column,
        column_name=column_name,
        stattest=stattest,
        threshold=threshold,
        column_type="cat",
    )


def calculate_data_drift_for_numeric_feature(
    reference_data: pd.DataFrame,
    current_data: pd.DataFrame,
    column_name: str,
    numeric_columns: List[str],
    stattest: Optional[PossibleStatTestType],
    threshold: Optional[float],
) -> Optional[DataDriftMetrics]:
    reference_column = reference_data[column_name]
    current_column = current_data[column_name]

    if not pd.api.types.is_numeric_dtype(reference_column) or not pd.api.types.is_numeric_dtype(current_column):
        raise ValueError(f"Column {column_name} should only contain numerical values.")

    result = calculate_data_drift(
        current_column=current_column,
        reference_column=reference_column,
        column_name=column_name,
        stattest=stattest,
        threshold=threshold,
        column_type="num",
    )
    result.current_correlations = current_data[numeric_columns + [column_name]].corr()[column_name].to_dict()
    result.reference_correlations = reference_data[numeric_columns + [column_name]].corr()[column_name].to_dict()
    return result


@dataclass
class DataDriftAnalyzerFeatureMetrics:
    current_small_hist: list
    ref_small_hist: list
    feature_type: str
    stattest_name: str
    p_value: float
    threshold: float
    drift_detected: bool


@dataclass
class DataDriftAnalyzerMetrics:
    n_features: int
    n_drifted_features: int
    share_drifted_features: float
    dataset_drift: bool
    features: Dict[str, DataDriftAnalyzerFeatureMetrics]


def dataset_drift_evaluation(p_values, drift_share=0.5) -> Tuple[int, float, bool]:
    n_drifted_features = sum([1 if x.drifted else 0 for _, x in p_values.items()])
    share_drifted_features = n_drifted_features / len(p_values)
    dataset_drift = bool(share_drifted_features >= drift_share)
    return n_drifted_features, share_drifted_features, dataset_drift


def get_overall_data_drift(
    current_data: pd.DataFrame,
    reference_data: pd.DataFrame,
    columns: DatasetColumns,
    data_drift_options: DataDriftOptions,
) -> DataDriftAnalyzerMetrics:
    num_feature_names = columns.num_feature_names
    cat_feature_names = columns.cat_feature_names
    target_column = columns.utility_columns.target
    prediction_column = columns.utility_columns.prediction
    drift_share = data_drift_options.drift_share
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
            columns.utility_columns.prediction = "predicted_labels"
            cat_feature_names += [columns.utility_columns.prediction]

        elif isinstance(prediction_column, list) and len(prediction_column) == 2:
            reference_data["prediction"] = reference_data[prediction_column[0]].values
            current_data["prediction"] = current_data[prediction_column[0]].values
            columns.utility_columns.prediction = "prediction"
            num_feature_names += [columns.utility_columns.prediction]

        elif isinstance(prediction_column, str):
            if (
                pd.api.types.is_numeric_dtype(reference_data[prediction_column].dtype)
                and reference_data[prediction_column].nunique() > 5
            ):
                num_feature_names += [prediction_column]
            else:
                cat_feature_names += [prediction_column]

    # calculate result
    features_metrics = {}
    p_values = {}

    for feature_name in num_feature_names:
        threshold = data_drift_options.get_threshold(feature_name)
        feature_type = "num"
        drift_result = calculate_data_drift(
            current_column=current_data[feature_name],
            reference_column=reference_data[feature_name],
            column_name=feature_name,
            stattest=data_drift_options.get_feature_stattest_func(feature_name, feature_type),
            threshold=threshold,
            column_type=feature_type,
        )

        p_values[feature_name] = PValueWithDrift(drift_result.drift_score, drift_result.drift_detected)
        current_nbinsx = data_drift_options.get_nbinsx(feature_name)
        features_metrics[feature_name] = DataDriftAnalyzerFeatureMetrics(
            current_small_hist=[
                t.tolist()
                for t in np.histogram(
                    current_data[feature_name][np.isfinite(current_data[feature_name])],
                    bins=current_nbinsx,
                    density=True,
                )
            ],
            ref_small_hist=[
                t.tolist()
                for t in np.histogram(
                    reference_data[feature_name][np.isfinite(reference_data[feature_name])],
                    bins=current_nbinsx,
                    density=True,
                )
            ],
            feature_type=feature_type,
            stattest_name=drift_result.stattest_name,
            p_value=drift_result.drift_score,
            drift_detected=drift_result.drift_detected,
            threshold=drift_result.threshold,
        )

    for feature_name in cat_feature_names:
        threshold = data_drift_options.get_threshold(feature_name)
        feature_ref_data = reference_data[feature_name].dropna()
        feature_cur_data = current_data[feature_name].dropna()

        feature_type = "cat"
        drift_result = calculate_data_drift(
            current_column=current_data[feature_name],
            reference_column=reference_data[feature_name],
            column_name=feature_name,
            stattest=data_drift_options.get_feature_stattest_func(feature_name, feature_type),
            threshold=threshold,
            column_type=feature_type,
        )
        p_values[feature_name] = PValueWithDrift(drift_result.drift_score, drift_result.drift_detected)

        ref_counts = feature_ref_data.value_counts(sort=False)
        cur_counts = feature_cur_data.value_counts(sort=False)
        keys = set(ref_counts.keys()).union(set(cur_counts.keys()))

        for key in keys:
            if key not in ref_counts:
                ref_counts.loc[key] = 0
            if key not in cur_counts:
                cur_counts.loc[key] = 0

        ref_small_hist = list(reversed(list(map(list, zip(*sorted(ref_counts.items(), key=lambda x: x[0]))))))
        cur_small_hist = list(reversed(list(map(list, zip(*sorted(cur_counts.items(), key=lambda x: x[0]))))))
        features_metrics[feature_name] = DataDriftAnalyzerFeatureMetrics(
            ref_small_hist=ref_small_hist,
            current_small_hist=cur_small_hist,
            feature_type=feature_type,
            stattest_name=drift_result.stattest_name,
            p_value=drift_result.drift_score,
            drift_detected=drift_result.drift_detected,
            threshold=drift_result.threshold,
        )

    n_drifted_features, share_drifted_features, dataset_drift = dataset_drift_evaluation(p_values, drift_share)
    return DataDriftAnalyzerMetrics(
        n_features=len(num_feature_names) + len(cat_feature_names),
        n_drifted_features=n_drifted_features,
        share_drifted_features=share_drifted_features,
        dataset_drift=dataset_drift,
        features=features_metrics,
    )


def calculate_column_data_drift(
    *,
    column_name: str,
    column_type: str,
    current_column: pd.Series,
    reference_column: pd.Series,
    drift_options: DataDriftOptions,
) -> DataDriftMetrics:
    """Calculate data drift for a single column."""
    stattest = drift_options.get_feature_stattest_func(column_name, column_type)
    threshold = drift_options.get_threshold(column_name)
    return calculate_data_drift(
        current_column=current_column,
        reference_column=reference_column,
        column_name=column_name,
        stattest=stattest,
        threshold=threshold,
        column_type=column_type,
    )


@dataclass
class DatasetDriftResults:
    options: DataDriftOptions
    columns: DatasetColumns
    metrics: DataDriftAnalyzerMetrics
    distr_for_plots: Dict[str, Dict[str, pd.DataFrame]]


def calculate_all_drifts_for_metrics(data, options: DataDriftOptions) -> DatasetDriftResults:
    """Calculate all drifts for all columns."""
    if data.current_data is None:
        raise ValueError("Current dataset should be present")

    if data.reference_data is None:
        raise ValueError("Reference dataset should be present")

    columns = process_columns(data.current_data, data.column_mapping)
    drift_metrics = get_overall_data_drift(
        current_data=data.current_data,
        reference_data=data.reference_data,
        columns=columns,
        data_drift_options=options,
    )
    distr_for_plots = {}

    for column_name in columns.num_feature_names:
        distr_for_plots[column_name] = get_distribution_for_column(
            column_name=column_name,
            column_type="num",
            current_data=data.current_data,
            reference_data=data.reference_data,
        )

    for column_name in columns.cat_feature_names:
        distr_for_plots[column_name] = get_distribution_for_column(
            column_name=column_name,
            column_type="cat",
            current_data=data.current_data,
            reference_data=data.reference_data,
        )

    return DatasetDriftResults(options=options, columns=columns, metrics=drift_metrics, distr_for_plots=distr_for_plots)
