import json
from datetime import datetime
from typing import List, Any, Dict

import pandas

from evidently.pipeline.pipeline import Pipeline
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.profile_sections.base_profile_section import ProfileSection
from evidently.utils import NumpyEncoder


class Profile(Pipeline):
    result: Dict[str, Any]

    def __init__(self, sections: List[ProfileSection]):
        super().__init__()
        self.parts = sections.copy()
        self.result = {}

    def calculate(self,
                  reference_data: pandas.DataFrame,
                  current_data: pandas.DataFrame,
                  column_mapping: ColumnMapping):
        self.execute(reference_data, current_data, column_mapping)
        self.result = {part.part_id(): part.calculate(reference_data, current_data, self.analyzers_results)
                       for part in self.parts}

    def get_analyzers(self):
        return list({analyzer for tab in self.parts for analyzer in tab.analyzers()})

    def json(self):
        return json.dumps(self.object(), cls=NumpyEncoder)

    def object(self):
        self.result["timestamp"] = str(datetime.now())
        return self.result
