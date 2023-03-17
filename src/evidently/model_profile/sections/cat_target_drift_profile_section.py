from datetime import datetime
from typing import Any
from typing import Dict
from typing import Iterable
from typing import Optional
from typing import Type

from evidently.analyzers.base_analyzer import Analyzer
from evidently.analyzers.cat_target_drift_analyzer import CatTargetDriftAnalyzer
from evidently.model_profile.sections.base_profile_section import ProfileSection


class CatTargetDriftProfileSection(ProfileSection):
    def part_id(self) -> str:
        return "cat_target_drift"

    def __init__(self) -> None:
        super().__init__()
        self.analyzers_types = [CatTargetDriftAnalyzer]
        self._result = None

    def analyzers(self) -> Iterable[Type[Analyzer]]:
        return self.analyzers_types

    def calculate(self, reference_data, current_data, column_mapping, analyzers_results) -> None:
        result = CatTargetDriftAnalyzer.get_results(analyzers_results)
        result_json: Dict[str, Any] = result.columns.dict(by_alias=True)
        result_json["metrics"] = {}

        if result.target_metrics:
            result_json["metrics"]["target_name"] = result.target_metrics.column_name
            result_json["metrics"]["target_type"] = "cat"
            result_json["metrics"]["target_drift"] = result.target_metrics.drift_score

        if result.prediction_metrics:
            result_json["metrics"]["prediction_name"] = result.prediction_metrics.column_name
            result_json["metrics"]["prediction_type"] = "cat"
            result_json["metrics"]["prediction_drift"] = result.prediction_metrics.drift_score

        self._result = {
            "name": self.part_id(),
            "datetime": str(datetime.now()),
            "data": result_json,
        }

    def get_results(self) -> Optional[dict]:
        return self._result
