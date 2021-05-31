import abc
from typing import List

from evidently.analyzers.base_analyzer import Analyzer


class ProfileSection:
    @abc.abstractmethod
    def analyzers(self) -> List[Analyzer]:
        raise NotImplementedError()

    @abc.abstractmethod
    def part_id(self) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def calculate(self, analyzer_results):
        raise NotImplementedError()
