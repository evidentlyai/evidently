from datetime import datetime

from evidently.analyzers.classification_performance_analyzer import ClassificationPerformanceAnalyzer
from evidently.analyzers.classification_performance_analyzer import ClassificationPerformanceMetrics
from evidently.model_profile.sections.base_profile_section import ProfileSection


class ClassificationPerformanceProfileSection(ProfileSection):
    def part_id(self) -> str:
        return "classification_performance"

    def __init__(self):
        super().__init__()
        self.analyzers_types = [ClassificationPerformanceAnalyzer]
        self._result = None

    def analyzers(self):
        return self.analyzers_types

    @staticmethod
    def _get_performance_metrics_as_dict(metrics: ClassificationPerformanceMetrics):
        return {
            "accuracy": metrics.accuracy,
            "precision": metrics.precision,
            "recall": metrics.recall,
            "f1": metrics.f1,
            "metrics_matrix": metrics.metrics_matrix,
            "confusion_matrix": {
                "labels": metrics.confusion_matrix.labels,
                "values": metrics.confusion_matrix.values,
            },
        }

    def calculate(self, reference_data, current_data, column_mapping, analyzers_results):
        result = ClassificationPerformanceAnalyzer.get_results(analyzers_results)
        result_for_json = result.columns.dict(by_alias=True)
        result_for_json["metrics"] = {}

        if result.reference_metrics:
            result_for_json["metrics"]["reference"] = self._get_performance_metrics_as_dict(result.reference_metrics)

        if result.current_metrics:
            result_for_json["metrics"]["current"] = self._get_performance_metrics_as_dict(result.current_metrics)

        self._result = {
            "name": self.part_id(),
            "datetime": str(datetime.now()),
            "data": result_for_json,
        }

    def get_results(self):
        return self._result
