from typing import List, Type

import pandas

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
        return self.analyzers_results
