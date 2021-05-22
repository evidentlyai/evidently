import json
from datetime import datetime
from typing import List, Type

from evidently.pipeline.pipeline import Pipeline
from evidently.profile_parts.base_profile_part import ProfilePart


class Profile(Pipeline):
    def __init__(self, parts: List[Type[ProfilePart]]):
        super().__init__()
        self.parts = [part() for part in parts]

    def get_analyzers(self):
        return list(set([analyzer for tab in self.parts for analyzer in tab.analyzers()]))

    def json(self):
        result = dict([(part.part_id(), part.calculate(self.analyzers_results)) for part in self.parts])
        result["timestamp"] = str(datetime.now())
        return json.dumps(result)