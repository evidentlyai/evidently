from datetime import datetime

import json

from evidently.analyzers.classification_performance_analyzer import ClassificationPerformanceAnalyzer
from evidently.profile_sections.base_profile_section import ProfileSection


class ClassificationPerformanceProfileSection(ProfileSection):
    def part_id(self) -> str:
        return 'classification_performance'

    def __init__(self):
        super().__init__()
        self.analyzers_types = [ClassificationPerformanceAnalyzer]

    def analyzers(self):
        return self.analyzers_types

    def calculate(self, analyzers_results):
        result = analyzers_results[ClassificationPerformanceAnalyzer]

        profile = {}
        profile['name'] = self.part_id()
        profile['datetime'] = str(datetime.now())
        profile['data'] = result

        return profile
