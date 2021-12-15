from datetime import datetime

from evidently.analyzers.data_drift_analyzer import DataDriftAnalyzer
from evidently.profile_sections.base_profile_section import ProfileSection


class DataDriftProfileSection(ProfileSection):
    def part_id(self) -> str:
        return "data_drift"

    def __init__(self):
        super().__init__()
        self.analyzers_types = [DataDriftAnalyzer]
        self._result = None

    def analyzers(self):
        return self.analyzers_types

    def calculate(self, reference_data, current_data, column_mapping, analyzers_results):
        result = analyzers_results[DataDriftAnalyzer]
        self._result = {
            'name': self.part_id(),
            'datetime': str(datetime.now()),
            'data': result
        }

    def get_results(self):
        return self._result
