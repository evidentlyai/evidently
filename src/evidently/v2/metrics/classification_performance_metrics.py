from evidently.analyzers.classification_performance_analyzer import ClassificationPerformanceAnalyzer
from evidently.analyzers.classification_performance_analyzer import ClassificationPerformanceMetrics
from evidently.analyzers.prob_classification_performance_analyzer import ProbClassificationPerformanceAnalyzer
from evidently.analyzers.prob_classification_performance_analyzer import ProbClassificationPerformanceMetrics
from evidently.options import QualityMetricsOptions
from evidently.options import OptionsProvider
from evidently.v2.metrics.base_metric import InputData
from evidently.v2.metrics.base_metric import Metric


ClassificationPerformanceMetricsResults = ClassificationPerformanceMetrics


class ClassificationPerformanceMetrics(Metric[ClassificationPerformanceMetricsResults]):
    def __init__(self):
        self.analyzer = ClassificationPerformanceAnalyzer()

    def calculate(self, data: InputData, metrics: dict) -> ClassificationPerformanceMetricsResults:
        if data.current_data is None:
            raise ValueError("current dataset should be present")

        analyzer_results = self.analyzer.calculate(
            reference_data=data.current_data,
            current_data=None,
            column_mapping=data.column_mapping
        )
        return analyzer_results.reference_metrics


ProbClassificationPerformanceMetricsResults = ProbClassificationPerformanceMetrics


class ProbClassificationPerformanceMetrics(Metric[ProbClassificationPerformanceMetricsResults]):
    def __init__(self, options: QualityMetricsOptions = None):
        self.analyzer = ProbClassificationPerformanceAnalyzer()
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
