import abc
from typing import List, Union

from dataclasses import dataclass

from evidently.v2.metrics.base_metric import Metric


@dataclass
class TestResult:
    name: str
    description: str
    status: str


class Test:
    @abc.abstractmethod
    def dependencies(self) -> List[Union[Metric, 'Test']]:
        return []

    @abc.abstractmethod
    def check(self, metrics: dict, tests: dict):
        raise NotImplementedError()
