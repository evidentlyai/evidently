import abc
from typing import Any
from typing import Dict
from typing import Iterable
from typing import Set
from typing import Type

import pandas

from evidently import ColumnMapping
from evidently.analyzers.base_analyzer import Analyzer
from evidently.options import OptionsProvider


class PipelineStage:
    _analyzers: Set[Type[Analyzer]]

    options_provider: OptionsProvider

    def __init__(self):
        self._analyzers = set()

    def add_analyzer(self, analyzer_type: Type[Analyzer]):
        self._analyzers.add(analyzer_type)

    def analyzers(self) -> Iterable[Type[Analyzer]]:
        return self._analyzers

    @abc.abstractmethod
    def calculate(
        self,
        reference_data: pandas.DataFrame,
        current_data: pandas.DataFrame,
        column_mapping: ColumnMapping,
        analyzers_results: Dict[Type[Analyzer], Any],
    ):
        raise NotImplementedError()
