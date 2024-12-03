import abc
import dataclasses
import uuid
from typing import Dict
from typing import Generic
from typing import List
from typing import Optional
from typing import Protocol
from typing import Tuple
from typing import TypeAlias
from typing import TypeVar
from typing import Union

from evidently.core import IncludeOptions
from evidently.model.dashboard import DashboardInfo
from evidently.model.widget import BaseWidgetInfo
from evidently.renderers.html_widgets import CounterData
from evidently.renderers.html_widgets import WidgetSize
from evidently.renderers.html_widgets import counter
from evidently.suite.base_suite import Display
from evidently.tests.base_test import TestStatus
from evidently.v2.datasets import Dataset


class MetricResult(Display):
    _widget: Optional[List[BaseWidgetInfo]] = None

    def set_widget(self, widget: List[BaseWidgetInfo]):
        self._widget = widget

    def _build_dashboard_info(self):
        return (
            "metric_" + str(uuid.uuid4()).replace("-", ""),
            DashboardInfo("Report", widgets=self._widget),
            {},
        )

    def as_dict(
        self,
        include_render: bool = False,
        include: Dict[str, IncludeOptions] = None,
        exclude: Dict[str, IncludeOptions] = None,
        **kwargs,
    ) -> dict:
        raise NotImplementedError()


TResult = TypeVar("TResult", bound=MetricResult)

MetricReturnValue: TypeAlias = Tuple[TResult, BaseWidgetInfo]


@dataclasses.dataclass
class CheckResult:
    name: str
    description: str
    status: TestStatus


class Check(Protocol[TResult]):
    def __call__(self, value: TResult) -> CheckResult: ...


class SingleValueCheck(Check[TResult], Protocol):
    def __call__(self, value: "SingleValue") -> CheckResult: ...


MetricId: TypeAlias = str


@dataclasses.dataclass
class SingleValue(MetricResult):
    value: Union[float, int, str]


def checks_widget(metric: "Metric", result: TResult) -> BaseWidgetInfo:
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
                for idx, check in enumerate([check(result) for check in metric.checks()])
            ],
        },
    )


def get_default_render(metric: "Metric", result: TResult) -> List[BaseWidgetInfo]:
    if isinstance(result, SingleValue):
        return [
            counter(
                title=metric.display_name(),
                size=WidgetSize.FULL,
                counters=[CounterData(label="", value=result.value)],
            ),
        ]
    raise NotImplementedError(f"No default render for {type(result)}")


class Metric(Generic[TResult]):
    _checks: List[Check]

    def call(self, current_data: Dataset, reference_data: Optional[Dataset]) -> TResult:
        result = self.calculate(current_data, reference_data)
        if result._widget is None:
            result._widget = get_default_render(self, result)
        if len(self._checks) > 0:
            result._widget.append(checks_widget(self, result))
        return result

    @abc.abstractmethod
    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> TResult:
        raise NotImplementedError()

    def id(self) -> MetricId:
        raise NotImplementedError()

    @abc.abstractmethod
    def display_name(self) -> str:
        raise NotImplementedError()

    def checks(self) -> List[Check]:
        return self._checks
