import json
from datetime import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence
from typing import Type

import pandas

from evidently.analyzers.base_analyzer import Analyzer
from evidently.model_profile.sections.base_profile_section import ProfileSection
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.pipeline.pipeline import Pipeline
from evidently.utils import NumpyEncoder


class Profile(Pipeline):
    result: Dict[str, Any]
    stages: Sequence[ProfileSection]

    def __init__(
        self, sections: Sequence[ProfileSection], options: Optional[list] = None
    ) -> None:
        if options is None:
            options = []
        super().__init__(sections, options if options is not None else [])

    def calculate(
        self,
        reference_data: pandas.DataFrame,
        current_data: Optional[pandas.DataFrame] = None,
        column_mapping: Optional[ColumnMapping] = None,
    ) -> None:
        self.execute(reference_data, current_data, column_mapping)

    def get_analyzers(self) -> List[Type[Analyzer]]:
        return list({analyzer for tab in self.stages for analyzer in tab.analyzers()})

    def json(self) -> str:
        return json.dumps(self.object(), cls=NumpyEncoder)

    def object(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            part.part_id(): part.get_results() for part in self.stages
        }
        result["timestamp"] = str(datetime.now())
        return result
