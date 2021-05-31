import json
import pandas 
from datetime import datetime
from typing import List, Type

from evidently.pipeline.pipeline import Pipeline
from evidently.profile_parts.base_profile_part import ProfilePart


class Profile(Pipeline):
    def __init__(self, parts: List[Type[ProfilePart]]):
        super().__init__()
        self.parts = [part() for part in parts]

    def calculate(self,
                  reference_data: pandas.DataFrame,
                  production_data: pandas.DataFrame,
                  column_mapping: dict = None):
        self.execute(reference_data, production_data, column_mapping)

    def get_analyzers(self):
        return list(set([analyzer for tab in self.parts for analyzer in tab.analyzers()]))

    def json(self):
        return json.dumps(self.object())

    def object(self):
        result = dict([(part.part_id(), part.calculate(self.analyzers_results)) for part in self.parts])
        result["timestamp"] = str(datetime.now())
        return result
