import dataclasses
from typing import Optional, Tuple

import numpy as np
import pandas as pd
from numpy import dtype

from evidently import ColumnMapping
from evidently.analyzers.classification_performance_analyzer import classification_performance_metrics
from evidently.analyzers import prob_classification_performance_analyzer as pcpa
from evidently.options import QualityMetricsOptions
from evidently.options import OptionsProvider
from evidently.v2.metrics.base_metric import InputData
from evidently.v2.metrics.base_metric import Metric


@dataclasses.dataclass
class ClassificationPerformanceMetricsResults:
    reference_metrics: Optional[pcpa.ProbClassificationPerformanceMetrics] = None
    current_metrics: Optional[pcpa.ProbClassificationPerformanceMetrics] = None
    dummy_metrics: Optional[pcpa.ProbClassificationPerformanceMetrics] = None


class ClassificationPerformanceMetrics(Metric[ClassificationPerformanceMetricsResults]):
    def __init__(self):
        pass

    def calculate(self, data: InputData, metrics: dict) -> ClassificationPerformanceMetricsResults:
        if data.current_data is None:
            raise ValueError("current dataset should be present")

        results = ClassificationPerformanceMetricsResults()
        current_data = _cleanup_data(data.current_data)
        target_data = current_data[data.column_mapping.target]
        prediction_data, pred_probas = get_prediction_data(current_data, data.column_mapping)
        results.current_metrics = classification_performance_metrics(target_data,
                                                                     prediction_data,
                                                                     data.column_mapping.target_names)

        if data.reference_data:
            reference_data = _cleanup_data(data.reference_data)
            ref_prediction_data, ref_pred_probas = get_prediction_data(reference_data, data.column_mapping)
            results.reference_metrics = classification_performance_metrics(
                reference_data[data.column_mapping.target],
                ref_prediction_data,
                data.column_mapping.target_names)

        dummy_preds = pd.Series([target_data.value_counts().argmax()] * len(target_data))
        results.dummy_metrics = classification_performance_metrics(target_data,
                                                                   dummy_preds,
                                                                   data.column_mapping.target_names)
        return results


def _cleanup_data(data: pd.DataFrame) -> pd.DataFrame:
    return data.replace([np.inf, -np.inf], np.nan).dropna(axis=0, how="any")


def get_prediction_data(data: pd.DataFrame, mapping: ColumnMapping) -> Tuple[pd.Series, Optional[pd.DataFrame]]:
    if isinstance(mapping.prediction, list):
        # list of columns with prediction probas, should be same as target labels
        return data[mapping.prediction].idxmax(axis=1), data[mapping.prediction]
    if isinstance(mapping.prediction, str) and data[mapping.prediction].dtype == dtype('float64'):
        predictions = data[mapping.prediction].apply(lambda x:
                                                     mapping.target_names[1] if x > 0.5 else mapping.target_names[0])
        prediction_probas = pd.DataFrame.from_dict({
            mapping.target_names[1]: data[mapping.prediction],
            mapping.target_names[0]: data[mapping.prediction].apply(lambda x: 1. - x)
        })
        return predictions, prediction_probas
    return data[mapping.prediction], None

ProbClassificationPerformanceMetricsResults = pcpa.ProbClassificationPerformanceMetrics


class ProbClassificationPerformanceMetrics(Metric[ProbClassificationPerformanceMetricsResults]):
    def __init__(self, options: QualityMetricsOptions = None):
        self.analyzer = pcpa.ProbClassificationPerformanceAnalyzer()
        self.analyzer.options_provider = OptionsProvider()

        if options is not None:
            self.analyzer.options_provider.add(options)

    def calculate(self, data: InputData, metrics: dict) -> ProbClassificationPerformanceMetricsResults:
        if data.current_data is None:
            raise ValueError("current dataset should be present")

        analyzer_results = self.analyzer.calculate(
            reference_data=data.current_data,
            current_data=None,
            column_mapping=data.column_mapping
        )
        return analyzer_results.reference_metrics
