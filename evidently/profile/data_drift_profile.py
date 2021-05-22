from typing import List, Type
from datetime import datetime

import pandas
import json

#from evidently.analyzers.base_analyzer import Analyzer
from evidently.analyzers.data_drift_analyzer import DataDriftAnalyzer
from evidently.pipeline.pipeline import Pipeline


class DataDriftProfile(Pipeline):
    def __init__(self):
        super().__init__()
        self.analyzers_types = [DataDriftAnalyzer]

    def get_analyzers(self):
        return self.analyzers_types

    def calculate(self,
                  reference_data: pandas.DataFrame,
                  production_data: pandas.DataFrame,
                  column_mapping: dict = None):
        self.execute(reference_data, production_data, column_mapping)

    def json(self):
        num_keys = self.analyzers_results[DataDriftAnalyzer]['num_features'].keys()
        num_pvalues = self.analyzers_results[DataDriftAnalyzer]['num_features']

        cat_keys = self.analyzers_results[DataDriftAnalyzer]['cat_features'].keys()
        cat_pvalues = self.analyzers_results[DataDriftAnalyzer]['cat_features']

        profile = {}
        profile['name'] = 'data_drift_profile'
        profile['datetime'] = str(datetime.now())
        profile['data'] = {}

        for key in num_keys:
            profile['data'][key] = {'feature_type' : num_pvalues[key]['feature_type'], 'p_value' : num_pvalues[key]['p_value']}

        for key in cat_keys:
            profile['data'][key] = {'feature_type' : cat_pvalues[key]['feature_type'], 'p_value' : cat_pvalues[key]['p_value']}

        return json.dumps(profile)
