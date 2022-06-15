import abc
from typing import Iterator

from evidently.v2.metrics.base_metric import Metric


class ExecutionGraph:
    @abc.abstractmethod
    def get_execution_iterator(self) -> Iterator[Metric]:
        raise NotImplementedError()


class SimpleExecutionGraph(ExecutionGraph):
    """
    Simple execution graph without any work with dependencies at all,
     assumes that metrics already in order for execution
    """
    def __init__(self, metrics: list[Metric]):
        self.metrics = metrics

    def get_execution_iterator(self) -> Iterator[Metric]:
        return self.metrics
