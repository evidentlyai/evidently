import abc
import functools
from typing import Dict
from typing import List
from typing import Tuple
from typing import Type

from evidently.metrics.base_metric import Metric
from evidently.tests.base_test import Test


class ExecutionGraph:
    @abc.abstractmethod
    def get_metric_execution_iterator(self) -> List[Tuple[Metric, Metric]]:
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

    def get_metric_execution_iterator(self) -> List[Tuple[Metric, Metric]]:
        aggregated: Dict[Type[Metric], List[Metric]] = functools.reduce(_aggregate_metrics, self.metrics, {})
        metric_to_calculations = {}
        for metric_type, metrics in aggregated.items():
            metrics_by_parameters: Dict[tuple, List[Metric]] = functools.reduce(_aggregate_by_parameters, metrics, {})

            for metric in metrics:
                metric_to_calculations[metric] = metrics_by_parameters[metric.get_parameters()][0]

        return [(metric, metric_to_calculations[metric]) for metric in self.metrics]

    def get_test_execution_iterator(self) -> List[Test]:
        return self.tests


def _aggregate_metrics(agg, item):
    agg[type(item)] = agg.get(type(item), []) + [item]
    return agg


def _aggregate_by_parameters(agg: dict, metric: Metric) -> dict:
    agg[metric.get_parameters()] = agg.get(metric.get_parameters(), []) + [metric]
    return agg
