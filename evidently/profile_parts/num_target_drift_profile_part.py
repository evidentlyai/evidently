from datetime import datetime

import json

from evidently.analyzers.num_target_drift_analyzer import NumTargetDriftAnalyzer
from evidently.profile_parts.base_profile_part import ProfilePart


class NumTargetDriftProfilePart(ProfilePart):
    def part_id(self) -> str:
        return 'num_target_drift'

    def __init__(self):
        super().__init__()
        self.analyzers_types = [NumTargetDriftAnalyzer]

    def analyzers(self):
        return self.analyzers_types

    def calculate(self, analyzers_results):
        result = analyzers_results[NumTargetDriftAnalyzer]

        profile = {}
        profile['name'] = self.part_id()
        profile['datetime'] = str(datetime.now())
        profile['data'] = result

        #if target_p_value:
        #profile['data']['target'] = {
        #    'target':target_name,
        #    'target_type':'num',
        #    'p_value':target_p_value,
        #    'correlations':target_corr
        #}

        #if prediction_p_value:
        #profile['data']['prediction'] = {
        #    'prediction':prediction_name,
        #    'prediction_type':'num',
        #    'p_value':prediction_p_value,
        #    'correlations':prediction_corr
        #}

        return profile
