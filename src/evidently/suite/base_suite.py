import copy
import dataclasses
import logging
from typing import Optional, Tuple, Iterator, Union

from evidently.metrics.base_metric import Metric, InputData
from evidently.renderers.base_renderer import TestRenderer, RenderersDefinitions, DEFAULT_RENDERERS, MetricRenderer
from evidently.suite.execution_graph import ExecutionGraph, SimpleExecutionGraph
from evidently.tests.base_test import Test, TestResult, GroupingTypes


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


def find_metric_renderer(obj, renderers: RenderersDefinitions) -> MetricRenderer:
    predefined = renderers.typed_renderers.get(obj, None)
    if predefined:
        return predefined
    if renderers.default_html_metric_renderer:
        return renderers.default_html_metric_renderer
    raise KeyError(f"No renderer found for {obj}")


def _discover_dependencies(test: Union[Metric, Test]) -> Iterator[Tuple[str, Union[Metric, Test]]]:
    for field_name, field in test.__dict__.items():
        if issubclass(type(field), (Metric, Test)):
            yield field_name, field


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

    def add_test(self, test: Test):
        test.set_context(self.context)
        for field_name, dependency in _discover_dependencies(test):
            if isinstance(dependency, Metric):
                self.add_metric(dependency)

            if isinstance(dependency, Test):
                dependency_copy = copy.copy(dependency)
                test.__setattr__(field_name, dependency_copy)
                self.add_test(dependency_copy)
        self.context.tests.append(test)
        self.context.state = States.Init

    def add_metric(self, metric: Metric):
        metric.set_context(self.context)
        for field_name, dependency in _discover_dependencies(metric):
            if isinstance(dependency, Metric):
                self.add_metric(dependency)

            if isinstance(dependency, Test):
                dependency_copy = copy.copy(dependency)
                metric.__setattr__(field_name, dependency_copy)
                self.add_test(dependency_copy)
        self.context.metrics.append(metric)
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

            calculations = {}
            for metric, calculation in execution_graph.get_metric_execution_iterator():
                if calculation not in calculations:
                    logging.debug(f"Executing {type(calculation)}...")
                    calculations[calculation] = calculation.calculate(data)
                else:
                    logging.debug(f"Using cached result for {type(calculation)}")
                results[metric] = calculations[calculation]

        self.context.metric_results = results
        self.context.state = States.Calculated

    def run_checks(self):
        if self.context.state in [States.Init, States.Verified]:
            raise ExecutionError("No calculation was made, run 'run_calculate' first'")

        test_results = {}

        for test in self.context.execution_graph.get_test_execution_iterator():
            try:
                logging.debug(f"Executing {type(test)}...")
                test_results[test] = test.check()
            except BaseException as ex:
                test_results[test] = TestResult(
                    name=test.name, status=TestResult.ERROR, description=f"Test failed with exceptions: {ex}"
                )
            test_results[test].groups.update(
                {
                    GroupingTypes.TestGroup.id: test.group,
                    GroupingTypes.TestType.id: test.name,
                }
            )

        self.context.test_results = test_results
        self.context.state = States.Tested
