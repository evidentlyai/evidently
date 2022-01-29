from datetime import datetime
from typing import Iterable
from typing import Optional
from typing import Type

from evidently.analyzers.base_analyzer import Analyzer
from evidently.analyzers.cat_target_drift_analyzer import CatTargetDriftAnalyzer
from evidently.model_profile.sections.base_profile_section import ProfileSection


class CatTargetDriftProfileSection(ProfileSection):
    def part_id(self) -> str:
        return 'cat_target_drift'

    def __init__(self) -> None:
        super().__init__()
        self.analyzers_types = [CatTargetDriftAnalyzer]
        self._result = None

    def analyzers(self) -> Iterable[Type[Analyzer]]:
        return self.analyzers_types

    def calculate(self, reference_data, current_data, column_mapping, analyzers_results) -> None:
        result = analyzers_results[CatTargetDriftAnalyzer]
        self._result = {
            'name': self.part_id(),
            'datetime': str(datetime.now()),
            'data': result
        }

    def get_results(self) -> Optional[dict]:
        return self._result
