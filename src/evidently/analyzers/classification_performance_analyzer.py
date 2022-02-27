#!/usr/bin/env python
# coding: utf-8
from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence
from typing import Union

import pandas as pd
import numpy as np
from dataclasses import dataclass
from sklearn import metrics

from evidently import ColumnMapping
from evidently.analyzers.base_analyzer import Analyzer
from evidently.analyzers.base_analyzer import BaseAnalyzerResult
from evidently.analyzers.utils import process_columns
from evidently.analyzers.utils import calculate_confusion_by_classes


@dataclass
class ConfusionMatrix:
    labels: List[str]
    values: list


@dataclass
class ClassificationPerformanceMetrics:
    """Class for classification performance metrics values"""

    accuracy: float
    precision: float
    recall: float
    f1: float
    metrics_matrix: Dict[str, Dict]
    confusion_matrix: ConfusionMatrix
    confusion_by_classes: Dict[str, Dict[str, int]]


@dataclass
class ClassificationPerformanceAnalyzerResults(BaseAnalyzerResult):
    reference_metrics: Optional[ClassificationPerformanceMetrics] = None
    current_metrics: Optional[ClassificationPerformanceMetrics] = None


def _calculate_performance_metrics(
    *,
    data: pd.DataFrame,
    target_column: Union[str, Sequence[str]],
    prediction_column: Union[str, Sequence[str]],
    target_names: Optional[List[str]],
) -> ClassificationPerformanceMetrics:
    # remove all rows with infinite and NaN values from the dataset
    data.replace([np.inf, -np.inf], np.nan, inplace=True)
    data.dropna(axis=0, how="any", inplace=True)

    # calculate metrics matrix
    metrics_matrix = metrics.classification_report(data[target_column], data[prediction_column], output_dict=True)
    # get quality metrics from the metrics matrix, do not calculate them again
    accuracy_score = metrics_matrix["accuracy"]
    avg_precision = metrics_matrix["macro avg"]["precision"]
    avg_recall = metrics_matrix["macro avg"]["recall"]
    avg_f1 = metrics_matrix["macro avg"]["f1-score"]

    # calculate confusion matrix
    confusion_matrix = metrics.confusion_matrix(data[target_column], data[prediction_column])
    # get labels from data mapping or get all values kinds from target and prediction columns
    labels = target_names if target_names else sorted(set(data[target_column]) | set(data[prediction_column]))
    confusion_by_classes = calculate_confusion_by_classes(confusion_matrix, labels)

    return ClassificationPerformanceMetrics(
        accuracy=accuracy_score,
        precision=avg_precision,
        recall=avg_recall,
        f1=avg_f1,
        metrics_matrix=metrics_matrix,
        confusion_matrix=ConfusionMatrix(labels=labels, values=confusion_matrix.tolist()),
        confusion_by_classes=confusion_by_classes,
    )


class ClassificationPerformanceAnalyzer(Analyzer):
    @staticmethod
    def get_results(analyzer_results) -> ClassificationPerformanceAnalyzerResults:
        return analyzer_results[ClassificationPerformanceAnalyzer]

    def calculate(
        self, reference_data: pd.DataFrame, current_data: Optional[pd.DataFrame], column_mapping: ColumnMapping
    ) -> ClassificationPerformanceAnalyzerResults:
        if reference_data is None:
            raise ValueError("reference_data should be present")

        columns = process_columns(reference_data, column_mapping)
        result = ClassificationPerformanceAnalyzerResults(columns=columns)
        target_column = columns.utility_columns.target
        prediction_column = columns.utility_columns.prediction
        target_names = columns.target_names

        if target_column is not None and prediction_column is not None:
            result.reference_metrics = _calculate_performance_metrics(
                data=reference_data,
                target_column=target_column,
                prediction_column=prediction_column,
                target_names=target_names,
            )

            if current_data is not None:
                result.current_metrics = _calculate_performance_metrics(
                    data=current_data,
                    target_column=target_column,
                    prediction_column=prediction_column,
                    target_names=target_names,
                )

        return result
