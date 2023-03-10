from datetime import datetime
from typing import Any
from typing import Dict

import pandas as pd

from evidently.analyzers.data_quality_analyzer import DataQualityAnalyzer
from evidently.calculations.data_quality import DataQualityStats
from evidently.model_profile.sections.base_profile_section import ProfileSection


class DataQualityProfileSection(ProfileSection):
    def part_id(self) -> str:
        return "data_quality"

    def __init__(self):
        super().__init__()
        self.analyzers_types = [DataQualityAnalyzer]
        self._result = None

    def analyzers(self):
        return self.analyzers_types

    @staticmethod
    def _get_stats_as_dict(all_features: DataQualityStats) -> Dict[str, Dict[str, Any]]:
        result: Dict[str, Dict[str, Any]] = {}

        for feature_name, feature_stats in all_features.get_all_features().items():
            result[feature_name] = {}

            for stat_name, stat_value in feature_stats.as_dict().items():
                if stat_value is not None:
                    result[feature_name][stat_name] = stat_value

        return result

    @staticmethod
    def _get_corr_matrices_as_dict(
        correlations: Dict[str, pd.DataFrame]
    ) -> Dict[str, Any]:
        result: Dict[str, Dict[str, Any]] = {}

        for kind, corr_df in correlations.items():
            result[kind] = {}
            for feature in corr_df.columns:
                result[kind][feature] = {
                    k: v
                    for (k, v) in zip(corr_df[feature].index, corr_df[feature])
                    if k != feature
                }

        return result

    def calculate(
        self, reference_data, current_data, column_mapping, analyzers_results
    ):
        result = DataQualityAnalyzer.get_results(analyzers_results)
        result_json = result.columns.as_dict()
        result_json["metrics"] = {}
        result_json["correlations"] = {}

        if result.reference_features_stats:
            result_json["metrics"]["reference"] = self._get_stats_as_dict(
                result.reference_features_stats
            )

        if result.current_features_stats:
            result_json["metrics"]["current"] = self._get_stats_as_dict(
                result.current_features_stats
            )

        if result.reference_correlations:
            result_json["correlations"]["reference"] = self._get_corr_matrices_as_dict(
                result.reference_correlations
            )

        if result.current_correlations:
            result_json["correlations"]["current"] = self._get_corr_matrices_as_dict(
                result.current_correlations
            )

        self._result = {
            "name": self.part_id(),
            "datetime": str(datetime.now()),
            "data": result_json,
        }

    def get_results(self):
        return self._result
