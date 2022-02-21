from datetime import datetime
from typing import Any
from typing import Dict

from dataclasses import fields

from evidently.analyzers.data_profile_analyzer import DataProfileAnalyzer
from evidently.analyzers.data_profile_analyzer import DataProfileStats
from evidently.analyzers.data_profile_analyzer import FeaturesProfileStats
from evidently.model_profile.sections.base_profile_section import ProfileSection


class DataProfileProfileSection(ProfileSection):
    def part_id(self) -> str:
        return "data_profile"

    def __init__(self):
        super().__init__()
        self.analyzers_types = [DataProfileAnalyzer]
        self._result = None

    def analyzers(self):
        return self.analyzers_types

    @staticmethod
    def _get_stats_as_dict(all_features: DataProfileStats) -> Dict[str, Dict[str, Any]]:
        result: Dict[str, Dict[str, Any]] = {}

        for feature_name, feature_stats in all_features.get_all_features().items():
            result[feature_name] = {}

            for stat_name, stat_value in feature_stats.as_dict().items():
                if stat_value is not None:
                    result[feature_name][stat_name] = stat_value

        return result

    def calculate(self, reference_data, current_data, column_mapping, analyzers_results):
        result = DataProfileAnalyzer.get_results(analyzers_results)
        result_json = result.columns.as_dict()
        result_json["metrics"] = {}

        if result.reference_features_stats:
            result_json["metrics"]["reference"] = self._get_stats_as_dict(result.reference_features_stats)

        if result.current_features_stats:
            result_json["metrics"]["current"] = self._get_stats_as_dict(result.current_features_stats)

        self._result = {"name": self.part_id(), "datetime": str(datetime.now()), "data": result_json}

    def get_results(self):
        return self._result
