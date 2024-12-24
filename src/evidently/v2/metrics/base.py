import abc
import dataclasses
import itertools
import typing
import uuid
from abc import abstractmethod
from copy import copy
from typing import Generic
from typing import List
from typing import Optional
from typing import Protocol
from typing import Tuple
from typing import TypeVar
from typing import Union

from IPython.core.display import HTML

from evidently.metric_results import Label
from evidently.model.dashboard import DashboardInfo
from evidently.model.widget import BaseWidgetInfo
from evidently.renderers.html_widgets import CounterData
from evidently.renderers.html_widgets import WidgetSize
from evidently.renderers.html_widgets import counter
from evidently.renderers.html_widgets import table_data
from evidently.tests.base_test import TestStatus
from evidently.utils.dashboard import TemplateParams
from evidently.utils.dashboard import inline_iframe_html_template
from evidently.v2.datasets import Dataset
from evidently.v2.datasets import DatasetColumn

if typing.TYPE_CHECKING:
    from evidently.v2.report import Context


class MetricResult:
    _metric: Optional["Metric"] = None
    _widget: Optional[List[BaseWidgetInfo]] = None
    _tests: Optional[List["MetricTestResult"]] = None

    def set_tests(self, tests: List["MetricTestResult"]):
        self._tests = tests

    def _repr_html_(self):
        assert self._widget
        widget = copy(self._widget)
        if self._tests:
            widget.append(metric_tests_widget(self.tests))
        return render_results(self, html=False)

    def is_widget_set(self) -> bool:
        return self._widget is not None

    @property
    def widget(self) -> List[BaseWidgetInfo]:
        return self._widget or []

    @widget.setter
    def widget(self, value: List[BaseWidgetInfo]):
        self._widget = value

    @property
    def tests(self) -> List["MetricTestResult"]:
        return self._tests or []


def render_widgets(widgets: List[BaseWidgetInfo]):
    dashboard_id, dashboard_info, graphs = (
        "metric_" + str(uuid.uuid4()).replace("-", ""),
        DashboardInfo("Report", widgets=widgets),
        {},
    )
    template_params = TemplateParams(
        dashboard_id=dashboard_id,
        dashboard_info=dashboard_info,
        additional_graphs=graphs,
    )
    return inline_iframe_html_template(template_params)


def render_results(results: Union[MetricResult, List[MetricResult]], html=True):
    data = []
    if isinstance(results, MetricResult):
        data = [results]
    else:
        data = results
    widgets = list(itertools.chain(*[item.widget for item in data]))
    result = render_widgets(widgets)
    if html:
        return HTML(result)
    return result


TResult = TypeVar("TResult", bound=MetricResult)

MetricReturnValue = Tuple[TResult, BaseWidgetInfo]

MetricTestId = str


@dataclasses.dataclass
class MetricTestResult:
    id: MetricTestId
    name: str
    description: str
    status: TestStatus


@dataclasses.dataclass
class SingleValue(MetricResult):
    value: Union[float, int, str]


@dataclasses.dataclass
class ByLabelValue(MetricResult):
    values: typing.Dict[Label, Union[float, int, bool, str]]


class MetricTest(Protocol[TResult]):
    def __call__(self, metric: "Metric", value: TResult) -> MetricTestResult: ...


class SingleValueMetricTest(MetricTest[SingleValue], Protocol):
    def __call__(self, metric: "Metric", value: SingleValue) -> MetricTestResult: ...


class ByLabelValueMetricTest(MetricTest[ByLabelValue], Protocol):
    def __call__(self, metric: "Metric", value: ByLabelValue) -> MetricTestResult: ...


MetricId = str

ByLabelValueTests = typing.Dict[Label, List[SingleValueMetricTest]]


def metric_tests_widget(tests: List[MetricTestResult]) -> BaseWidgetInfo:
    return BaseWidgetInfo(
        title="",
        size=2,
        type="test_suite",
        params={
            "tests": [
                dict(
                    title=test.name,
                    description=test.description,
                    state=test.status.value.lower(),
                    groups=[],
                )
                for idx, test in enumerate(tests)
            ],
        },
    )


def get_default_render(title: str, result: TResult) -> List[BaseWidgetInfo]:
    if isinstance(result, SingleValue):
        return [
            counter(
                title=title,
                size=WidgetSize.FULL,
                counters=[CounterData(label="", value=str(result.value))],
            ),
        ]
    if isinstance(result, ByLabelValue):
        return [
            table_data(title=title, column_names=["Label", "Value"], data=[(k, v) for k, v in result.values.items()])
        ]
    raise NotImplementedError(f"No default render for {type(result)}")


class Metric(Generic[TResult]):
    """
    Base metric class.

    Metric is class to perform calculation over given dataset and return result.
    """

    _metric_id: MetricId
    _tests: Optional[List[MetricTest[TResult]]]

    def __init__(self, metric_id: MetricId) -> None:
        self._metric_id = metric_id
        self._tests = None

    def call(self, context: "Context") -> TResult:
        """
        main method is used for executing metric
        Args:
            context:
        Returns:

        """
        result = self._call(context)
        if not result.is_widget_set():
            result.widget = get_default_render(self.display_name(), result)
        if self._tests and len(self._tests) > 0:
            result.set_tests([test(self, result) for test in self._tests])
        return result

    def _call(self, context: "Context") -> TResult:
        return self.calculate(*context._input_data)

    @abc.abstractmethod
    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> TResult:
        raise NotImplementedError()

    def _default_tests(self) -> List[MetricTest[TResult]]:
        """
        allows to redefine default tests for metric
        Returns:
            list of tests to use as default
        """
        return []

    def _default_tests_with_reference(self) -> Optional[List[MetricTest[TResult]]]:
        """
        allows to redefine default tests for metric when calculated with reference
        Returns:
            list of tests to use as default when called with reference data
            None - if default tests should be returned
        """
        return None

    @property
    def id(self) -> MetricId:
        return self._metric_id

    @abc.abstractmethod
    def display_name(self) -> str:
        raise NotImplementedError()

    def with_tests(self, tests: Optional[List[MetricTest[TResult]]]):
        self._tests = tests
        return self

    def tests(self) -> List[MetricTest[TResult]]:
        return self._tests or []

    def group_by(self, group_by: Optional[str]) -> Union["Metric", List["Metric"]]:
        if group_by is None:
            return self
        raise NotImplementedError()


MetricV2 = Metric


class ColumnMetric(Metric[TResult]):
    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> TResult:
        return self.calculate_value(
            current_data.column(self.column_name),
            reference_data.column(self.column_name) if reference_data else None,
        )

    @abstractmethod
    def calculate_value(self, current_data: DatasetColumn, reference_data: Optional[DatasetColumn]) -> TResult:
        raise NotImplementedError()

    def display_name(self) -> str:
        raise NotImplementedError()

    def __init__(self, column_name: str, metric_id: MetricId):
        super().__init__(metric_id)
        self._column_name = column_name

    @property
    def column_name(self) -> str:
        return self._column_name
