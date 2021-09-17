from datetime import datetime

from evidently.analyzers.cat_target_drift_analyzer import CatTargetDriftAnalyzer
from evidently.profile_sections.base_profile_section import ProfileSection


class CatTargetDriftProfileSection(ProfileSection):
    def part_id(self) -> str:
        return 'cat_target_drift'

    def __init__(self):
        super().__init__()
        self.analyzers_types = [CatTargetDriftAnalyzer]

    def analyzers(self):
        return self.analyzers_types

    def calculate(self, analyzers_results):
        result = analyzers_results[CatTargetDriftAnalyzer]
        return {
            'name': self.part_id(),
            'datetime': str(datetime.now()),
            'data': result
        }
