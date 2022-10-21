from abc import ABC
from typing import Optional
from typing import Tuple
from typing import Union

import numpy as np
import pandas as pd

from evidently import ColumnMapping
from evidently.calculations.classification_performance import PredictionData
from evidently.calculations.classification_performance import get_prediction_data
from evidently.calculations.classification_performance import k_probability_threshold
from evidently.metrics.base_metric import Metric
from evidently.metrics.base_metric import TResult
from evidently.utils.data_operations import DatasetColumns
from evidently.utils.data_operations import process_columns


def _cleanup_data(data: pd.DataFrame, dataset_columns: DatasetColumns) -> pd.DataFrame:
    target = dataset_columns.utility_columns.target
    prediction = dataset_columns.utility_columns.prediction
    subset = []
    if target is not None:
        subset.append(target)
    if prediction is not None and isinstance(prediction, list):
        subset += prediction
    if prediction is not None and isinstance(prediction, str):
        subset.append(prediction)
    if len(subset) > 0:
        return data.replace([np.inf, -np.inf], np.nan).dropna(axis=0, how="any", subset=subset)
    return data


class ThresholdClassificationMetric(Metric[TResult], ABC):
    def __init__(self, threshold: Optional[float], k: Optional[Union[float, int]]):
        if threshold is not None and k is not None:
            raise ValueError(f"{self.__class__.__name__}: should provide only threshold or top_k argument, not both.")
        self.threshold = threshold
        self.k = k

    def get_target_prediction_data(
        self,
        data: pd.DataFrame,
        column_mapping: ColumnMapping,
    ) -> Tuple[pd.Series, PredictionData]:
        dataset_columns = process_columns(data, column_mapping)
        data = _cleanup_data(data, dataset_columns)
        prediction = get_prediction_data(data, dataset_columns, column_mapping.pos_label)
        if self.threshold is None and self.k is None:
            return data[dataset_columns.utility_columns.target], prediction
        if len(prediction.labels) > 2 or prediction.prediction_probas is None:
            raise ValueError("Top K / Threshold parameter can be used only with binary classification with probas")
        pos_label, neg_label = prediction.prediction_probas.columns
        threshold = self.threshold
        if self.k is not None:
            threshold = k_probability_threshold(prediction.prediction_probas, self.k)
        prediction_labels = prediction.prediction_probas[pos_label].apply(
            lambda x: pos_label if x >= threshold else neg_label
        )
        return data[dataset_columns.utility_columns.target], PredictionData(
            predictions=prediction_labels,
            prediction_probas=prediction.prediction_probas,
            labels=prediction.labels,
        )
