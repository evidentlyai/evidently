import abc
from typing import Iterator, List

from evidently.v2.metrics.base_metric import Metric
from evidently.v2.tests.base_test import Test


class ExecutionGraph:
    @abc.abstractmethod
    def get_metric_execution_iterator(self) -> Iterator[Metric]:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_test_execution_iterator(self) -> Iterator[Test]:
        raise NotImplementedError()


class SimpleExecutionGraph(ExecutionGraph):
    """
    Simple execution graph without any work with dependencies at all,
     assumes that metrics already in order for execution
    """

    metrics: List[Metric]
    tests: List[Test]

    def __init__(self, metrics: List[Metric], tests: List[Test]):
        self.metrics = metrics
        self.tests = tests

    def get_metric_execution_iterator(self) -> Iterator[Metric]:
        return self.metrics

    def get_test_execution_iterator(self) -> Iterator[Test]:
        return self.tests
