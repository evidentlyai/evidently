from datetime import datetime

from evidently.analyzers.prob_classification_performance_analyzer import ProbClassificationPerformanceAnalyzer
from evidently.analyzers.prob_classification_performance_analyzer import ProbClassificationPerformanceMetrics
from evidently.model_profile.sections.base_profile_section import ProfileSection


class ProbClassificationPerformanceProfileSection(ProfileSection):
    def part_id(self) -> str:
        return "probabilistic_classification_performance"

    def __init__(self):
        super().__init__()
        self.analyzers_types = [ProbClassificationPerformanceAnalyzer]
        self._result = None

    def analyzers(self):
        return self.analyzers_types

    @staticmethod
    def _get_regression_performance_metrics_as_dict(metrics: ProbClassificationPerformanceMetrics) -> dict:
        result = {
            "accuracy": metrics.accuracy,
            "precision": metrics.precision,
            "recall": metrics.recall,
            "f1": metrics.f1,
            "pr_curve": metrics.pr_curve,
            "pr_table": metrics.pr_table,
            "roc_auc": metrics.roc_auc,
            "roc_curve": metrics.roc_curve,
            "log_loss": metrics.log_loss,
            "metrics_matrix": metrics.metrics_matrix,
            "confusion_matrix": {
                "labels": metrics.confusion_matrix.labels,
                "values": metrics.confusion_matrix.values,
            },
        }

        if metrics.roc_aucs is not None:
            result["roc_aucs"] = metrics.roc_aucs

        return result

    def calculate(self, reference_data, current_data, column_mapping, analyzers_results):
        result = ProbClassificationPerformanceAnalyzer.get_results(analyzers_results)
        result_json = result.columns.dict(by_alias=True)
        result_json["options"] = result.quality_metrics_options.as_dict()
        result_json["metrics"] = {}

        if result.reference_metrics is not None:
            result_json["metrics"]["reference"] = self._get_regression_performance_metrics_as_dict(
                result.reference_metrics
            )

        if result.current_metrics is not None:
            result_json["metrics"]["current"] = self._get_regression_performance_metrics_as_dict(result.current_metrics)

        self._result = {
            "name": self.part_id(),
            "datetime": str(datetime.now()),
            "data": result_json,
        }

    def get_results(self):
        return self._result
