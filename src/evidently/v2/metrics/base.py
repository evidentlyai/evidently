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

from evidently.model.dashboard import DashboardInfo
from evidently.model.widget import BaseWidgetInfo
from evidently.pydantic_utils import EvidentlyBaseModel
from evidently.renderers.html_widgets import CounterData
from evidently.renderers.html_widgets import WidgetSize
from evidently.renderers.html_widgets import counter
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
    _checks: Optional[List["CheckResult"]] = None

    def set_checks(self, checks: List["CheckResult"]):
        self._checks = checks

    def _repr_html_(self):
        assert self._widget
        widget = copy(self._widget)
        if self._checks:
            widget.append(checks_widget(self))
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
    def checks(self) -> List["CheckResult"]:
        return self._checks


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

CheckId = str


@dataclasses.dataclass
class CheckResult:
    id: CheckId
    name: str
    description: str
    status: TestStatus


@dataclasses.dataclass
class SingleValue(MetricResult):
    value: Union[float, int, str]


class Check(Protocol[TResult]):
    def __call__(self, metric: "Metric", value: TResult) -> CheckResult: ...


class SingleValueCheck(Check[TResult], Protocol):
    def __call__(self, metric: "Metric", value: SingleValue) -> CheckResult: ...


MetricId = str


def checks_widget(result: TResult) -> BaseWidgetInfo:
    return BaseWidgetInfo(
        title="",
        size=2,
        type="test_suite",
        params={
            "tests": [
                dict(
                    title=check.name,
                    description=check.description,
                    state=check.status.value.lower(),
                    groups=[],
                )
                for idx, check in enumerate(result.checks)
            ],
        },
    )


def get_default_render(title: str, result: TResult) -> List[BaseWidgetInfo]:
    if isinstance(result, SingleValue):
        return [
            counter(
                title=title,
                size=WidgetSize.FULL,
                counters=[CounterData(label="", value=result.value)],
            ),
        ]
    raise NotImplementedError(f"No default render for {type(result)}")


class Metric(EvidentlyBaseModel, Generic[TResult]):
    """
    Base metric class.

    Metric is class to perform calculation over given dataset and return result.
    """

    class Config:
        alias_required = False  # todo: turn on

    metric_id: MetricId
    _checks: Optional[List[Check]]

    def __init__(self, metric_id: MetricId, checks: Optional[List[Check]] = None, **data) -> None:
        self.metric_id = metric_id
        self._checks = checks
        super().__init__(**data)

    def call(self, context: "Context") -> TResult:
        """
        main method is used for executing metric
        Args:
            context:
        Returns:

        """
        result = self.calculate(*context._input_data)
        if not result.is_widget_set():
            result.widget = get_default_render(self.display_name(), result)
        if self._checks and len(self._checks) > 0:
            result.set_checks([check(self, result) for check in self._checks])
        return result

    @abc.abstractmethod
    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> TResult:
        raise NotImplementedError()

    def _default_checks(self) -> List[Check]:
        """
        allows to redefine default checks for metric
        Returns:
            list of checks to use as default
        """
        return []

    def _default_checks_with_reference(self) -> Optional[List[Check]]:
        """
        allows to redefine default checks for metric when calculated with reference
        Returns:
            list of checks to use as default when called with reference data
            None - if default checks should be returned
        """
        return None

    @property
    def id(self) -> MetricId:
        return self.metric_id

    @abc.abstractmethod
    def display_name(self) -> str:
        raise NotImplementedError()

    def checks(self) -> List[Check]:
        return self._checks or []

    def group_by(self, group_by: Optional[str]) -> Union["Metric", List["Metric"]]:
        if group_by is None:
            return self
        raise NotImplementedError()


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