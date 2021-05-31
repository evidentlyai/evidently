from datetime import datetime

import json

from evidently.analyzers.regression_performance_analyzer import RegressionPerformanceAnalyzer
from evidently.profile_sections.base_profile_section import ProfileSection


class RegressionPerformanceProfileSection(ProfileSection):
    def part_id(self) -> str:
        return 'regression_performance'

    def __init__(self):
        super().__init__()
        self.analyzers_types = [RegressionPerformanceAnalyzer]

    def analyzers(self):
        return self.analyzers_types

    def calculate(self, analyzers_results):
        result = analyzers_results[RegressionPerformanceAnalyzer]

        profile = {}
        profile['name'] = self.part_id()
        profile['datetime'] = str(datetime.now())
        profile['data'] = result

        return profile
