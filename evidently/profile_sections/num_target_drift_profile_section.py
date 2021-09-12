from datetime import datetime

from evidently.analyzers.num_target_drift_analyzer import NumTargetDriftAnalyzer
from evidently.profile_sections.base_profile_section import ProfileSection


class NumTargetDriftProfileSection(ProfileSection):
    def part_id(self) -> str:
        return 'num_target_drift'

    def __init__(self):
        super().__init__()
        self.analyzers_types = [NumTargetDriftAnalyzer]

    def analyzers(self):
        return self.analyzers_types

    def calculate(self, analyzers_results):
        result = analyzers_results[NumTargetDriftAnalyzer]

        return {
            'name': self.part_id(),
            'datetime': str(datetime.now()),
            'data': result
        }
