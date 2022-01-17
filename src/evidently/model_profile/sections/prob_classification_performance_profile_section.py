from datetime import datetime

from evidently.analyzers.prob_classification_performance_analyzer import ProbClassificationPerformanceAnalyzer
from evidently.model_profile.sections.base_profile_section import ProfileSection


class ProbClassificationPerformanceProfileSection(ProfileSection):
    def part_id(self) -> str:
        return 'probabilistic_classification_performance'

    def __init__(self):
        super().__init__()
        self.analyzers_types = [ProbClassificationPerformanceAnalyzer]
        self._result = None

    def analyzers(self):
        return self.analyzers_types

    def calculate(self, reference_data, current_data, column_mapping, analyzers_results):
        result = analyzers_results[ProbClassificationPerformanceAnalyzer]

        self._result = {
            'name': self.part_id(),
            'datetime': str(datetime.now()),
            'data': result
        }

    def get_results(self):
        return self._result
