import itertools
from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence
from typing import Type

import pandas

from evidently.analyzers.base_analyzer import Analyzer
from evidently.options import OptionsProvider
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.pipeline.stage import PipelineStage


class Pipeline:
    _analyzers: List[Type[Analyzer]]
    stages: Sequence[PipelineStage]
    analyzers_results: Dict[Type[Analyzer], object]
    options_provider: OptionsProvider

    def __init__(self, stages: Sequence[PipelineStage], options: list):
        self.stages = stages
        self.analyzers_results = {}
        self.options_provider = OptionsProvider()
        self._analyzers = list(
            itertools.chain.from_iterable([stage.analyzers() for stage in stages])
        )
        for option in options:
            self.options_provider.add(option)

    def get_analyzers(self) -> List[Type[Analyzer]]:
        return self._analyzers

    def execute(
        self,
        reference_data: pandas.DataFrame,
        current_data: Optional[pandas.DataFrame] = None,
        column_mapping: Optional[ColumnMapping] = None,
    ) -> None:
        if column_mapping is None:
            column_mapping = ColumnMapping()

        #  making shallow copy - this copy DOES NOT copy existing data, but contains link to it:
        #  - this copy WILL DISCARD all columns changes or rows changes (adding or removing)
        #  - this copy WILL KEEP all values' changes in existing rows and columns.
        rdata = reference_data.copy()
        cdata = None if current_data is None else current_data.copy()
        for analyzer in self.get_analyzers():
            instance = analyzer()
            instance.options_provider = self.options_provider
            self.analyzers_results[analyzer] = instance.calculate(
                rdata, cdata, column_mapping
            )
        for stage in self.stages:
            stage.options_provider = self.options_provider
            stage.calculate(
                rdata.copy(),
                None if cdata is None else cdata.copy(),
                column_mapping,
                self.analyzers_results,
            )
