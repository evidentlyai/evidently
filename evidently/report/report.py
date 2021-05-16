from typing import List, Type

import pandas

from evidently.analyzes.base_analyze import Analyze
from evidently.pipeline.pipeline import Pipeline


class Report(Pipeline):
    def __init__(self, analyzes_types: List[Type[Analyze]]):
        super().__init__()
        self.analyzes_types = analyzes_types

    def get_analyzes(self):
        return self.analyzes_types

    def calculate(self,
                  reference_data: pandas.DataFrame,
                  production_data: pandas.DataFrame,
                  column_mapping: dict = None):
        self.execute(reference_data, production_data, column_mapping)

    def json(self):
        return self.analyzes_results
