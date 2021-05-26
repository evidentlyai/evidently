from datetime import datetime

import json

from evidently.analyzers.data_drift_analyzer import DataDriftAnalyzer
from evidently.profile_parts.base_profile_part import ProfilePart


class DataDriftProfilePart(ProfilePart):
    def part_id(self) -> str:
        return "data_drift"

    def __init__(self):
        super().__init__()
        self.analyzers_types = [DataDriftAnalyzer]

    def analyzers(self):
        return self.analyzers_types

    def calculate(self, analyzers_results):
        num_keys = analyzers_results[DataDriftAnalyzer]['num_features'].keys()
        num_pvalues = analyzers_results[DataDriftAnalyzer]['num_features']

        cat_keys = analyzers_results[DataDriftAnalyzer]['cat_features'].keys()
        cat_pvalues = analyzers_results[DataDriftAnalyzer]['cat_features']

        profile = {}
        profile['name'] = self.part_id()
        profile['datetime'] = str(datetime.now())
        profile['data'] = {}

        for key in num_keys:
            profile['data'][key] = {'feature_type' : num_pvalues[key]['feature_type'], 'p_value' : num_pvalues[key]['p_value']}

        for key in cat_keys:
            profile['data'][key] = {'feature_type' : cat_pvalues[key]['feature_type'], 'p_value' : cat_pvalues[key]['p_value']}

        return profile
