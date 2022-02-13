#!/usr/bin/env python
# coding: utf-8
from typing import List
from typing import Optional
from typing import Dict

import pandas as pd
import numpy as np
from dataclasses import dataclass
from sklearn import metrics

from evidently import ColumnMapping
from evidently.analyzers.base_analyzer import Analyzer
from evidently.analyzers.base_analyzer import BaseAnalyzerResult
from evidently.analyzers.utils import process_columns


@dataclass
class ConfusionMatrix:
    labels: List[str]
    values: list


@dataclass
class PerformanceMetrics:
    """Class for performance metrics values"""
    accuracy: float
    precision: float
    recall: float
    f1: float
    metrics_matrix: Dict[str, Dict]
    confusion_matrix: ConfusionMatrix
    confusion_by_classes: Dict[str, Dict[str, int]]


@dataclass
class ClassificationPerformanceAnalyzerResults(BaseAnalyzerResult):
    reference_metrics: Optional[PerformanceMetrics] = None
    current_metrics: Optional[PerformanceMetrics] = None


def _calculate_performance_metrics(
        *, data: pd.DataFrame, target_column: str, prediction_column: str, target_names: List[str]
) -> PerformanceMetrics:
    data.replace([np.inf, -np.inf], np.nan, inplace=True)
    data.dropna(axis=0, how='any', inplace=True)

    # calculate quality metrics
    accuracy_score = metrics.accuracy_score(data[target_column], data[prediction_column])
    avg_precision = metrics.precision_score(data[target_column], data[prediction_column], average='macro')
    avg_recall = metrics.recall_score(data[target_column], data[prediction_column], average='macro')
    avg_f1 = metrics.f1_score(data[target_column], data[prediction_column], average='macro')

    # calculate class support and metrics matrix
    metrics_matrix = metrics.classification_report(
        data[target_column],
        data[prediction_column],
        output_dict=True)

    # calculate confusion matrix
    confusion_matrix = metrics.confusion_matrix(data[target_column], data[prediction_column])
    labels = target_names if target_names else sorted(set(data[target_column]))

    # get TP, FP, TN, FN metrics for each class
    false_positive = confusion_matrix.sum(axis=0) - np.diag(confusion_matrix)
    false_negative = confusion_matrix.sum(axis=1) - np.diag(confusion_matrix)
    true_positive = np.diag(confusion_matrix)
    true_negative = confusion_matrix.sum() - (false_positive + false_negative + true_positive)
    confusion_by_classes = {}

    for idx, class_name in enumerate(labels):
        confusion_by_classes[str(class_name)] = {
            'tp': true_positive[idx],
            'tn': true_negative[idx],
            'fp': false_positive[idx],
            'fn': false_negative[idx],
        }

    return PerformanceMetrics(
        accuracy=accuracy_score,
        precision=avg_precision,
        recall=avg_recall,
        f1=avg_f1,
        metrics_matrix=metrics_matrix,
        confusion_matrix=ConfusionMatrix(labels=labels, values=confusion_matrix.tolist()),
        confusion_by_classes=confusion_by_classes
    )


class ClassificationPerformanceAnalyzer(Analyzer):
    @staticmethod
    def get_results(analyzer_results) -> ClassificationPerformanceAnalyzerResults:
        return analyzer_results[ClassificationPerformanceAnalyzer]

    def calculate(self,
                  reference_data: pd.DataFrame,
                  current_data: Optional[pd.DataFrame],
                  column_mapping: ColumnMapping) -> ClassificationPerformanceAnalyzerResults:
        if reference_data is None:
            raise ValueError('reference_data should be present')

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
                target_names=target_names
            )

            if current_data is not None:
                result.current_metrics = _calculate_performance_metrics(
                    data=current_data,
                    target_column=target_column,
                    prediction_column=prediction_column,
                    target_names=target_names
                )

        return result
