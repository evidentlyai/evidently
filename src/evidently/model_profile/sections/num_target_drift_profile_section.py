from datetime import datetime

from evidently.analyzers.num_target_drift_analyzer import NumTargetDriftAnalyzer
from evidently.model_profile.sections.base_profile_section import ProfileSection


class NumTargetDriftProfileSection(ProfileSection):
    def part_id(self) -> str:
        return "num_target_drift"

    def __init__(self):
        super().__init__()
        self.analyzers_types = [NumTargetDriftAnalyzer]
        self._result = None

    def analyzers(self):
        return self.analyzers_types

    def calculate(
        self, reference_data, current_data, column_mapping, analyzers_results
    ):
        result = NumTargetDriftAnalyzer.get_results(analyzers_results)
        result_json = result.columns.as_dict()
        result_json["metrics"] = {}

        if result.target_metrics:
            result_json["metrics"]["target_name"] = result.target_metrics.column_name
            result_json["metrics"]["target_type"] = "num"
            result_json["metrics"]["target_drift"] = result.target_metrics.drift_score
            result_json["metrics"]["target_correlations"] = {
                "current": result.target_metrics.current_correlations,
                "reference": result.target_metrics.reference_correlations,
            }

        if result.prediction_metrics:
            result_json["metrics"][
                "prediction_name"
            ] = result.prediction_metrics.column_name
            result_json["metrics"]["prediction_type"] = "num"
            result_json["metrics"][
                "prediction_drift"
            ] = result.prediction_metrics.drift_score
            result_json["metrics"]["prediction_correlations"] = {
                "current": result.prediction_metrics.current_correlations,
                "reference": result.prediction_metrics.reference_correlations,
            }

        self._result = {
            "name": self.part_id(),
            "datetime": str(datetime.now()),
            "data": result_json,
        }

    def get_results(self):
        return self._result
