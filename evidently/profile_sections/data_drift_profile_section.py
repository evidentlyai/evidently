from datetime import datetime

from evidently.analyzers.data_drift_analyzer import DataDriftAnalyzer
from evidently.profile_sections.base_profile_section import ProfileSection


class DataDriftProfileSection(ProfileSection):
    def part_id(self) -> str:
        return "data_drift"

    def __init__(self):
        super().__init__()
        self.analyzers_types = [DataDriftAnalyzer]

    def analyzers(self):
        return self.analyzers_types

    def calculate(self, analyzers_results):
        result = analyzers_results[DataDriftAnalyzer]
        return {
            'name': self.part_id(),
            'datetime': str(datetime.now()),
            'data': result
        }
