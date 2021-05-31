from datetime import datetime

import json

from evidently.analyzers.prob_classification_performance_analyzer import ProbClassificationPerformanceAnalyzer
from evidently.profile_sections.base_profile_section import ProfileSection


class ProbClassificationPerformanceProfileSection(ProfileSection):
    def part_id(self) -> str:
        return 'probabilistic_classification_performance'

    def __init__(self):
        super().__init__()
        self.analyzers_types = [ProbClassificationPerformanceAnalyzer]

    def analyzers(self):
        return self.analyzers_types

    def calculate(self, analyzers_results):
        result = analyzers_results[ProbClassificationPerformanceAnalyzer]

        profile = {}
        profile['name'] = self.part_id()
        profile['datetime'] = str(datetime.now())
        profile['data'] = result

        return profile
