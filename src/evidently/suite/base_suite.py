import abc
import copy
import json
import logging
from typing import Iterator
from typing import Optional
from typing import Tuple
from typing import Union

import dataclasses

from evidently.dashboard.dashboard import SaveMode
from evidently.dashboard.dashboard import SaveModeMap
from evidently.dashboard.dashboard import TemplateParams
from evidently.dashboard.dashboard import save_data_file
from evidently.dashboard.dashboard import save_lib_files
from evidently.metrics.base_metric import ErrorResult
from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.renderers.base_renderer import DEFAULT_RENDERERS
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import RenderersDefinitions
from evidently.renderers.base_renderer import TestRenderer
from evidently.renderers.notebook_utils import determine_template
from evidently.suite.execution_graph import ExecutionGraph
from evidently.suite.execution_graph import SimpleExecutionGraph
from evidently.tests.base_test import GroupingTypes
from evidently.tests.base_test import Test
from evidently.tests.base_test import TestResult
from evidently.utils import NumpyEncoder


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


class Display:
    @abc.abstractmethod
    def _build_dashboard_info(self):
        raise NotImplementedError()

    def _repr_html_(self):
        dashboard_id, dashboard_info, graphs = self._build_dashboard_info()
        template_params = TemplateParams(
            dashboard_id=dashboard_id, dashboard_info=dashboard_info, additional_graphs=graphs
        )
        return self._render(determine_template("auto"), template_params)

    def show(self, mode="auto"):
        dashboard_id, dashboard_info, graphs = self._build_dashboard_info()
        template_params = TemplateParams(
            dashboard_id=dashboard_id, dashboard_info=dashboard_info, additional_graphs=graphs
        )
        # pylint: disable=import-outside-toplevel
        try:
            from IPython.display import HTML

            return HTML(self._render(determine_template(mode), template_params))
        except ImportError as err:
            raise Exception("Cannot import HTML from IPython.display, no way to show html") from err

    def save_html(self, filename: str, mode: Union[str, SaveMode] = SaveMode.SINGLE_FILE):
        dashboard_id, dashboard_info, graphs = self._build_dashboard_info()
        if isinstance(mode, str):
            _mode = SaveModeMap.get(mode)
            if _mode is None:
                raise ValueError(f"Unexpected save mode {mode}. Expected [{','.join(SaveModeMap.keys())}]")
            mode = _mode
        if mode == SaveMode.SINGLE_FILE:
            template_params = TemplateParams(
                dashboard_id=dashboard_id,
                dashboard_info=dashboard_info,
                additional_graphs=graphs,
            )
            with open(filename, "w", encoding="utf-8") as out_file:
                out_file.write(self._render(determine_template("inline"), template_params))
        else:
            font_file, lib_file = save_lib_files(filename, mode)
            data_file = save_data_file(filename, mode, dashboard_id, dashboard_info, graphs)
            template_params = TemplateParams(
                dashboard_id=dashboard_id,
                dashboard_info=dashboard_info,
                additional_graphs=graphs,
                embed_lib=False,
                embed_data=False,
                embed_font=False,
                font_file=font_file,
                include_js_files=[lib_file, data_file],
            )
            with open(filename, "w", encoding="utf-8") as out_file:
                out_file.write(self._render(determine_template("inline"), template_params))

    @abc.abstractmethod
    def as_dict(self) -> dict:
        raise NotImplementedError()

    def json(self) -> str:
        return json.dumps(self.as_dict(), cls=NumpyEncoder)

    def save_json(self, filename):
        with open(filename, "w", encoding="utf-8") as out_file:
            json.dump(self.as_dict(), out_file, cls=NumpyEncoder)

    def _render(self, temple_func, template_params: TemplateParams):
        return temple_func(params=template_params)


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

        if self.context.execution_graph is not None:
            execution_graph: ExecutionGraph = self.context.execution_graph

            calculations = {}
            for metric, calculation in execution_graph.get_metric_execution_iterator():
                if calculation not in calculations:
                    logging.debug(f"Executing {type(calculation)}...")
                    try:
                        calculations[calculation] = calculation.calculate(data)
                    except BaseException as ex:
                        calculations[calculation] = ErrorResult(ex)
                else:
                    logging.debug(f"Using cached result for {type(calculation)}")
                self.context.metric_results[metric] = calculations[calculation]

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
