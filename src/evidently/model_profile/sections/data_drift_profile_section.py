from datetime import datetime
from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

from evidently.analyzers.data_drift_analyzer import DataDriftAnalyzer
from evidently.model_profile.sections.base_profile_section import ProfileSection


class DataDriftProfileSection(ProfileSection):
    def part_id(self) -> str:
        return "data_drift"

    def __init__(self):
        super().__init__()
        self.analyzers_types = [DataDriftAnalyzer]
        self._result = None

    def analyzers(self):
        return self.analyzers_types

    def calculate(
        self, reference_data, current_data, column_mapping, analyzers_results
    ) -> None:
        data_drift_results = DataDriftAnalyzer.get_results(analyzers_results)
        result_json: Dict[str, Any] = data_drift_results.columns.as_dict()

        metrics_dict: Dict[str, Union[int, bool, float, Dict]] = {
            "n_features": data_drift_results.metrics.number_of_columns,
            "n_drifted_features": data_drift_results.metrics.number_of_drifted_columns,
            "share_drifted_features": data_drift_results.metrics.share_of_drifted_columns,
            "dataset_drift": data_drift_results.metrics.dataset_drift,
        }
        # add metrics to a flat dict with data drift results
        for (
            feature_name,
            feature_metrics,
        ) in data_drift_results.metrics.drift_by_columns.items():
            metrics_dict[feature_name] = {
                "current_small_hist": feature_metrics.current_small_distribution,
                "ref_small_hist": feature_metrics.reference_small_distribution,
                "feature_type": feature_metrics.column_type,
                "stattest_name": feature_metrics.stattest_name,
                "drift_score": feature_metrics.drift_score,
                "drift_detected": feature_metrics.drift_detected,
            }

        result_json["options"] = data_drift_results.options.as_dict()
        result_json["metrics"] = metrics_dict

        self._result = {
            "name": self.part_id(),
            "datetime": str(datetime.now()),
            "data": result_json,
        }

    def get_results(self) -> Optional[Dict[str, Union[str, Dict]]]:
        return self._result
