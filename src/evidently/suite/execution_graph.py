import abc
from typing import List

from evidently.metrics.base_metric import Metric
from evidently.tests.base_test import Test


class ExecutionGraph:
    @abc.abstractmethod
    def get_metric_execution_iterator(self) -> List[Metric]:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_test_execution_iterator(self) -> List[Test]:
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

    def get_metric_execution_iterator(self) -> List[Metric]:
        return self.metrics

    def get_test_execution_iterator(self) -> List[Test]:
        return self.tests
