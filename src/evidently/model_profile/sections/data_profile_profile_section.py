from datetime import datetime

from evidently.analyzers.data_profile_analyzer import DataProfileAnalyzer
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

    def calculate(self, reference_data, current_data, column_mapping, analyzers_results):
        result = DataProfileAnalyzer.get_results(analyzers_results)
        result_json = result.columns.as_dict()
        result_json['metrics'] = {}

        if result.reference_features_stats:
            result_json['metrics']['reference'] = result.reference_features_stats

        if result.current_features_stats:
            result_json['metrics']['current'] = result.current_features_stats

        self._result = {
            'name': self.part_id(),
            'datetime': str(datetime.now()),
            'data': result_json
        }

    def get_results(self):
        return self._result
