import abc
from typing import Iterable, Type

import pandas

from evidently.analyzers.base_analyzer import Analyzer
from evidently.pipeline.stage import PipelineStage


class ProfileSection(PipelineStage):
    @abc.abstractmethod
    def analyzers(self) -> Iterable[Type[Analyzer]]:
        raise NotImplementedError()

    @abc.abstractmethod
    def part_id(self) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def calculate(self, reference_data: pandas.DataFrame,
                  current_data: pandas.DataFrame,
                  column_mapping,
                  analyzers_results):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_results(self):
        raise NotImplementedError()
