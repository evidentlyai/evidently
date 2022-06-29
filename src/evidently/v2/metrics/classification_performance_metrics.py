import dataclasses
from typing import Optional

import pandas as pd

from evidently.analyzers import classification_performance_analyzer as cpa
from evidently.analyzers.classification_performance_analyzer import ClassificationPerformanceAnalyzer, \
    ClassificationPerformanceAnalyzerResults, classification_performance_metrics
from evidently.analyzers import prob_classification_performance_analyzer as pcpa
from evidently.options import QualityMetricsOptions
from evidently.options import OptionsProvider
from evidently.v2.metrics.base_metric import InputData
from evidently.v2.metrics.base_metric import Metric


@dataclasses.dataclass
class ClassificationPerformanceMetricsResults(ClassificationPerformanceAnalyzerResults):
    dummy_metrics: Optional[cpa.ClassificationPerformanceMetrics] = None


class ClassificationPerformanceMetrics(Metric[ClassificationPerformanceMetricsResults]):
    def __init__(self):
        self.analyzer = ClassificationPerformanceAnalyzer()

    def calculate(self, data: InputData, metrics: dict) -> ClassificationPerformanceMetricsResults:
        if data.current_data is None:
            raise ValueError("current dataset should be present")

        if data.reference_data is None:
            analyzer_results = self.analyzer.calculate(
                reference_data=data.current_data,
                current_data=None,
                column_mapping=data.column_mapping
            )
            analyzer_results.current_metrics = analyzer_results.reference_metrics
            analyzer_results.reference_metrics = None
        else:
            analyzer_results = self.analyzer.calculate(
                reference_data=data.reference_data,
                current_data=data.current_data,
                column_mapping=data.column_mapping
            )
        results = ClassificationPerformanceMetricsResults(**analyzer_results.__dict__)
        target_data = data.current_data[data.column_mapping.target]
        dummy_preds = pd.Series([target_data.value_counts().argmax()] * len(target_data))
        results.dummy_metrics = classification_performance_metrics(target_data,
                                                                   dummy_preds,
                                                                   data.column_mapping.target_names)
        return results


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
