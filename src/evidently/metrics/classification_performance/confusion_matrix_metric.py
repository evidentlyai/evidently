import dataclasses
from typing import Union, Optional, List

import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix

from evidently import ColumnMapping
from evidently.calculations.classification_performance import k_probability_threshold, ConfusionMatrix, \
    get_prediction_data
from evidently.metrics.base_metric import Metric, InputData

DEFAULT_THRESHOLD = 0.5


@dataclasses.dataclass
class ClassificationConfusionMatrixResult:
    current_matrix: ConfusionMatrix
    reference_matrix: ConfusionMatrix


def _cleanup_data(data: pd.DataFrame, mapping: ColumnMapping) -> pd.DataFrame:
    target = mapping.target
    prediction = mapping.prediction
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


class ClassificationConfusionMatrix(Metric[ClassificationConfusionMatrixResult]):
    def __init__(self, threshold: Optional[float], k: Optional[Union[float, int]]):
        if threshold is not None and k is not None:
            raise f"{self.__class__.__name__}: should provide only threshold or top_k argument, not both."
        self.threshold = threshold
        self.k = k

    def calculate(self, data: InputData) -> ClassificationConfusionMatrixResult:
        current_data = _cleanup_data(data.current_data, data.column_mapping)

        prediction = get_prediction_data(data.current_data, data.column_mapping)

        predicted_labels, probas = self._get_prediction(
            prediction.predictions,
            prediction.prediction_probas,
            prediction.labels,
        )

        current_results = self._calculate_matrix(
            current_data[data.column_mapping.target],
            predicted_labels,
            prediction.labels,
        )

        reference_results = None
        if data.reference_data is not None:
            reference_data = _cleanup_data(data.reference_data, data.column_mapping)
            ref_preds = get_prediction_data(data.reference_data, data.column_mapping)
            predicted_labels, probas = self._get_prediction(
                ref_preds.predictions,
                ref_preds.prediction_probas,
                ref_preds.labels
            )
            reference_results = self._calculate_matrix(
                reference_data[data.column_mapping.target],
                predicted_labels,
                prediction.labels,
            )

        return ClassificationConfusionMatrixResult(
            current_matrix=current_results,
            reference_matrix=reference_results,
        )

    @staticmethod
    def _calculate_matrix(
        target: pd.Series,
        prediction: pd.Series,
        labels: List[str, int]
    ) -> ConfusionMatrix:
        matrix = confusion_matrix(target, prediction, labels=labels)
        return ConfusionMatrix(labels, matrix)

    def _get_prediction(
        self,
        prediction_data: pd.Series,
        prediction_probas: Optional[pd.DataFrame],
        labels: List[str],
    ):
        if self.threshold is None and self.k is None:
            return prediction_data, prediction_probas
        if len(labels) > 2 or prediction_probas is None:
            raise ValueError("Top K / Threshold parameter can be used only with binary classification with probas")
        pos_label, neg_label = prediction_probas.columns
        threshold = self.threshold
        if self.k is not None:
            threshold = k_probability_threshold(prediction_probas, self.k)
        prediction_labels = prediction_probas[pos_label].apply(lambda x: pos_label if x >= threshold else neg_label)
        return prediction_labels, prediction_probas
