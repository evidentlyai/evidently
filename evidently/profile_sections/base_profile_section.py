import abc

import pandas

from evidently.pipeline.stage import PipelineStage


class ProfileSection(PipelineStage):
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
