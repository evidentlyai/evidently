import dataclasses

from evidently.v2.metrics.base_metric import Metric, InputData
from evidently.v2.suite.execution_graph import ExecutionGraph
from evidently.v2.tests.base_test import Test


@dataclasses.dataclass
class State:
    name: str


class States:
    Init = State("Init")
    Verified = State("Verified")
    Calculated = State("Calculated")
    Tested = State("Tested")


class Context:
    """Pipeline execution context tracks pipeline execution and lifecycle"""
    execution_graph: ExecutionGraph
    metric_results: dict
    test_results: dict
    state: PipelineState


class BaseSuite:
    def __init__(self):
        pass

    def add_metric(self, metric: Metric):
        pass

    def add_test(self, test: Test):
        pass

    def verify(self):
        pass

    def run_calculate(self, data: InputData):
        pass

    def run_checks(self):
        pass
