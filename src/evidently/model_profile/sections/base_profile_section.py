import abc
from typing import Any
from typing import Dict
from typing import Iterable
from typing import Optional
from typing import Type

import pandas

from evidently.analyzers.base_analyzer import Analyzer
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.pipeline.stage import PipelineStage


class ProfileSection(PipelineStage):
    _result: Optional[dict]

    @abc.abstractmethod
    def analyzers(self) -> Iterable[Type[Analyzer]]:
        raise NotImplementedError()

    @abc.abstractmethod
    def part_id(self) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def calculate(
        self,
        reference_data: pandas.DataFrame,
        current_data: Optional[pandas.DataFrame],
        column_mapping: ColumnMapping,
        analyzers_results: Dict[Type[Analyzer], Any],
    ) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_results(self) -> Optional[dict]:
        raise NotImplementedError()
