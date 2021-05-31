from datetime import datetime

import json

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

        profile = {}
        profile['name'] = self.part_id()
        profile['datetime'] = str(datetime.now())
        profile['data'] = result

        #if target_p_value:
        #profile['data']['target_drift'] = {
        #    'target': target_name,
        #    'target_type':'cat',
        #    'p_value':target_p_value
        #}

        #if prediction_p_value:
        #profile['data']['prediction_drift'] = {
        #    'prediction': prediction_name,
        #    'prediction_type':'cat',
        #    'p_value':prediction_p_value
        #}

        return profile
