import json
from datetime import datetime
from typing import Any, Dict, Sequence, Optional

import pandas

from evidently.pipeline.pipeline import Pipeline
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.profile_sections.base_profile_section import ProfileSection
from evidently.utils import NumpyEncoder


class Profile(Pipeline):
    result: Dict[str, Any]
    stages: Sequence[ProfileSection]

    def __init__(self, sections: Sequence[ProfileSection], options: Optional[list] = None):
        super().__init__(sections, options if options is not None else [])

    def calculate(self,
                  reference_data: pandas.DataFrame,
                  current_data: pandas.DataFrame,
                  column_mapping: ColumnMapping):
        self.execute(reference_data, current_data, column_mapping)

    def get_analyzers(self):
        return list({analyzer for tab in self.stages for analyzer in tab.analyzers()})

    def json(self):
        return json.dumps(self.object(), cls=NumpyEncoder)

    def object(self):
        result = {
            part.part_id(): part.get_results() for part in self.stages
        }
        result["timestamp"] = str(datetime.now())
        return result
