import abc
from typing import List, Dict, Type

import pandas

from evidently.analyzers.base_analyzer import Analyzer
from evidently.pipeline.column_mapping import ColumnMapping


class Pipeline:
    analyzers_results: Dict[Type[Analyzer], object]

    def __init__(self):
        self.analyzers_results = {}

    @abc.abstractmethod
    def get_analyzers(self) -> List[Type[Analyzer]]:
        raise NotImplementedError("get_analyzers should be implemented")

    def execute(self,
                reference_data: pandas.DataFrame,
                current_data: pandas.DataFrame,
                column_mapping: ColumnMapping = None):
        if column_mapping is None:
            column_mapping = ColumnMapping()
        for analyzer in self.get_analyzers():
            self.analyzers_results[analyzer] =\
                analyzer().calculate(reference_data, current_data, column_mapping)
