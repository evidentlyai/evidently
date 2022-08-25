"""Methods for data drift calculations"""

from typing import List, Optional, Dict
from typing import Optional
from typing import Sequence
from typing import Union

import numpy as np
import pandas as pd
from dataclasses import dataclass

from evidently.analyzers.stattests.registry import get_stattest
from evidently.analyzers.stattests.registry import PossibleStatTestType
from evidently.analyzers.stattests.registry import StatTest


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


def _compute_statistic(
    reference_data: pd.DataFrame,
    current_data: pd.DataFrame,
    feature_type: str,
    column_name: str,
    stattest: StatTest,
    threshold: Optional[float],
):
    return stattest(reference_data[column_name], current_data[column_name], feature_type, threshold)


@dataclass
class DataDriftMetrics:
    """Class for drift values"""

    column_name: str
    stattest_name: str
    drift_score: float
    drift_detected: bool
    # correlations for numeric features
    reference_correlations: Optional[Dict[str, float]] = None
    current_correlations: Optional[Dict[str, float]] = None


def calculate_data_drift(
    *,
    current_data: pd.DataFrame,
    reference_data: pd.DataFrame,
    column_name: str,
    stattest: Optional[PossibleStatTestType],
    threshold: float,
    feature_type: str,
) -> DataDriftMetrics:
    drift_test_function = get_stattest(reference_data[column_name], current_data[column_name], feature_type, stattest)
    drift_result = drift_test_function(reference_data[column_name], current_data[column_name], feature_type, threshold)
    return DataDriftMetrics(
        column_name=column_name,
        stattest_name=drift_test_function.display_name,
        drift_score=drift_result.drift_score,
        drift_detected=drift_result.drifted,
    )


def calculate_data_drift_for_category_feature(
    *,
    current_data: pd.DataFrame,
    reference_data: pd.DataFrame,
    column_name: str,
    stattest: Optional[PossibleStatTestType],
    threshold: float,
):
    return calculate_data_drift(
        current_data=current_data.dropna(subset=[column_name]),
        reference_data=reference_data.dropna(subset=[column_name]),
        column_name=column_name,
        stattest=stattest,
        threshold=threshold,
        feature_type="cat",
    )


def calculate_data_drift_for_numeric_feature(
    reference_data: pd.DataFrame,
    current_data: pd.DataFrame,
    column_name: str,
    numeric_columns: List[str],
    stattest: StatTest,
    threshold: float,
) -> Optional[DataDriftMetrics]:
    if not pd.api.types.is_numeric_dtype(reference_data[column_name]) or not pd.api.types.is_numeric_dtype(
        current_data[column_name]
    ):
        raise ValueError(f"Column {column_name} should only contain numerical values.")

    result = calculate_data_drift(
        current_data=current_data,
        reference_data=reference_data,
        column_name=column_name,
        stattest=stattest,
        threshold=threshold,
        feature_type="num",
    )
    result.current_correlations = current_data[numeric_columns + [column_name]].corr()[column_name].to_dict()
    result.reference_correlations = reference_data[numeric_columns + [column_name]].corr()[column_name].to_dict()
    return result
