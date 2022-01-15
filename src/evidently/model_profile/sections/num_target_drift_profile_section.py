from datetime import datetime

from evidently.analyzers.num_target_drift_analyzer import NumTargetDriftAnalyzer
from evidently.model_profile.sections.base_profile_section import ProfileSection


class NumTargetDriftProfileSection(ProfileSection):
    def part_id(self) -> str:
        return 'num_target_drift'

    def __init__(self):
        super().__init__()
        self.analyzers_types = [NumTargetDriftAnalyzer]
        self._result = None

    def analyzers(self):
        return self.analyzers_types

    def calculate(self, reference_data, current_data, column_mapping, analyzers_results):
        result = analyzers_results[NumTargetDriftAnalyzer]

        self._result = {
            'name': self.part_id(),
            'datetime': str(datetime.now()),
            'data': result
        }

    def get_results(self):
        return self._result
