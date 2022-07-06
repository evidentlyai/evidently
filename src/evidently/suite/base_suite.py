import dataclasses
from typing import Optional

from evidently.metrics.base_metric import Metric, InputData
from evidently.renderers.base_renderer import TestRenderer, RenderersDefinitions, DEFAULT_RENDERERS
from evidently.suite.execution_graph import ExecutionGraph, SimpleExecutionGraph
from evidently.tests.base_test import Test


@dataclasses.dataclass
class State:
    name: str


class States:
    Init = State("Init")
    Verified = State("Verified")
    Calculated = State("Calculated")
    Tested = State("Tested")


def find_test_renderer(obj, renderers: RenderersDefinitions) -> TestRenderer:
    predefined = renderers.typed_renderers.get(obj, None)
    if predefined:
        return predefined
    if issubclass(obj, Test) and renderers.default_html_test_renderer:
        return renderers.default_html_test_renderer
    raise KeyError(f"No renderer found for {obj}")


@dataclasses.dataclass
class Context:
    """Pipeline execution context tracks pipeline execution and lifecycle"""

    execution_graph: Optional[ExecutionGraph]
    metrics: list
    tests: list
    metric_results: dict
    test_results: dict
    state: State
    renderers: RenderersDefinitions


class ExecutionError(Exception):
    pass


class Suite:
    context: Context

    def __init__(self):
        self.context = Context(
            execution_graph=None,
            metrics=[],
            tests=[],
            metric_results={},
            test_results={},
            state=States.Init,
            renderers=DEFAULT_RENDERERS,
        )

    def add_metrics(self, *metrics: Metric):
        for metric in metrics:
            metric.set_context(self.context)
        self.context.metrics.extend(metrics)
        self.context.state = States.Init

    def add_tests(self, *tests: Test):
        for test in tests:
            test.set_context(self.context)
        self.context.tests.extend(tests)
        self.context.state = States.Init

    def verify(self):
        self.context.execution_graph = SimpleExecutionGraph(self.context.metrics, self.context.tests)
        self.context.state = States.Verified

    def run_calculate(self, data: InputData):
        if self.context.state in [States.Init]:
            self.verify()

        if self.context.state in [States.Calculated, States.Tested]:
            return

        results: dict = {}

        if self.context.execution_graph is not None:
            execution_graph: ExecutionGraph = self.context.execution_graph

            for metric in execution_graph.get_metric_execution_iterator():
                results[metric] = metric.calculate(data, results)

        self.context.metric_results = results
        self.context.state = States.Calculated

    def run_checks(self):
        if self.context.state in [States.Init, States.Verified]:
            raise ExecutionError("No calculation was made, run 'run_calculate' first'")

        test_results = {}

        for test in self.context.execution_graph.get_test_execution_iterator():
            test_results[test] = test.check()

        self.context.test_results = test_results
        self.context.state = States.Tested
