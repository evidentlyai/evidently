import abc
from typing import List

import pandas

from evidently.analyzers.base_analyzer import Analyzer


class ProfileSection:
    @abc.abstractmethod
    def analyzers(self) -> List[Analyzer]:
        raise NotImplementedError()

    @abc.abstractmethod
    def part_id(self) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def calculate(self, reference_data: pandas.DataFrame, current_data: pandas.DataFrame, analyzers_results):
        raise NotImplementedError()
