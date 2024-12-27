import abc
import dataclasses
import inspect
import itertools
import typing
import uuid
from abc import ABC
from abc import abstractmethod
from copy import copy
from typing import Generator
from typing import Generic
from typing import List
from typing import Optional
from typing import Protocol
from typing import Tuple
from typing import TypeVar
from typing import Union

import typing_inspect

from evidently.metric_results import Label
from evidently.model.dashboard import DashboardInfo
from evidently.model.widget import BaseWidgetInfo
from evidently.pydantic_utils import EvidentlyBaseModel
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
        try:
            from IPython.core.display import HTML

            return HTML(result)
        except ImportError as err:
            raise Exception("Cannot import HTML from IPython.display, no way to show html") from err
    return result


TResult = TypeVar("TResult", bound=MetricResult)

MetricReturnValue = Tuple[TResult, BaseWidgetInfo]

MetricTestId = str

Value = Union[float, int, str]


@dataclasses.dataclass
class MetricTestResult:
    id: MetricTestId
    name: str
    description: str
    status: TestStatus


@dataclasses.dataclass
class SingleValue(MetricResult):
    value: Value


@dataclasses.dataclass
class ByLabelValue(MetricResult):
    values: typing.Dict[Label, Value]

    def labels(self) -> List[Label]:
        return list(self.values.keys())

    def get_label_result(self, label: Label) -> SingleValue:
        value = self.values.get(label)
        return SingleValue(value)


@dataclasses.dataclass
class CountValue(MetricResult):
    count: int
    share: float

    def get_count(self) -> SingleValue:
        return SingleValue(self.count)

    def get_share(self) -> SingleValue:
        return SingleValue(self.share)


class MetricTest(Protocol[TResult]):
    def __call__(self, metric: "Metric", value: TResult) -> MetricTestResult: ...


class SingleValueMetricTest(MetricTest[SingleValue], Protocol):
    def __call__(self, metric: "Metric", value: SingleValue) -> MetricTestResult: ...


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
    if isinstance(result, CountValue):
        return [
            counter(
                title=f"{title}: count",
                size=WidgetSize.HALF,
                counters=[CounterData(label="", value=str(result.count))],
            ),
            counter(
                title=f"{title}: share",
                size=WidgetSize.HALF,
                counters=[CounterData(label="", value=f"{result.share:.2f}")],
            ),
        ]
    raise NotImplementedError(f"No default render for {type(result)}")


class Metric(Generic[TResult]):
    """
    Base metric class.

    Metric is class to perform calculation over given dataset and return result.
    """

    _metric_id: MetricId

    def __init__(self, metric_id: MetricId) -> None:
        self._metric_id = metric_id

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
        test_results = list(self.get_tests(result))
        if test_results and len(test_results) > 0:
            result.set_tests(test_results)
        return result

    def _call(self, context: "Context") -> TResult:
        return self.calculate(*context._input_data)

    @abc.abstractmethod
    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> TResult:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_tests(self, value: TResult) -> Generator[MetricTestResult, None, None]:
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

    def group_by(self, group_by: Optional[str]) -> Union["Metric", List["Metric"]]:
        if group_by is None:
            return self
        raise NotImplementedError()


class AutoAliasMixin:
    __alias_type__: typing.ClassVar[str]

    @classmethod
    def __get_type__(cls):
        config = cls.__dict__.get("Config")
        if config is not None and config.__dict__.get("type_alias") is not None:
            return config.type_alias
        return f"evidently:{cls.__alias_type__}:{cls.__name__}"


class MetricConfig(AutoAliasMixin, EvidentlyBaseModel):
    __alias_type__: typing.ClassVar[str] = "metric_config"

    class Config:
        is_base_type = True

    __metric_type__: typing.Type["MetricWithConfig"]

    def __get_metric_type__(self) -> typing.Type["MetricWithConfig"]:
        if not hasattr(self, "__metric_type__"):
            raise ValueError(f"{self.__class__.__name__} is not binded to Metric type")
        return self.__metric_type__

    def to_metric(self) -> "MetricWithConfig":
        metric_type = self.__get_metric_type__()
        return metric_type(self.get_metric_id(), self)

    def get_metric_id(self) -> str:
        return self.get_fingerprint()


TConfig = TypeVar("TConfig", bound=MetricConfig)


class MetricWithConfig(Metric[TResult], Generic[TResult, TConfig], abc.ABC):
    def __init__(self, metric_id: MetricId, config: TConfig):
        self.config = config
        super().__init__(metric_id)

    def __init_subclass__(cls):
        if not inspect.isabstract(cls):
            base = typing_inspect.get_generic_bases(cls)[0]  # fixme only works for simple cases
            config_type = typing_inspect.get_args(base)[1]
            if not issubclass(config_type, MetricConfig):
                raise ValueError("Value of generic parameter TConfig should be MetricConfig subclass")
            config_type.__metric_type__ = cls
        super().__init_subclass__()


class ColumnMetricConfig(MetricConfig, abc.ABC):
    column_name: str


TColumnConfig = TypeVar("TColumnConfig", bound=ColumnMetricConfig)


class ColumnMetric(MetricWithConfig[TResult, TColumnConfig]):
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

    @property
    def column_name(self) -> str:
        return self.config.column_name


class SingleValueMetric(Metric[SingleValue], ABC):
    _tests: Optional[List[MetricTest[SingleValue]]]

    def with_tests(self, tests: Optional[List[MetricTest[SingleValue]]]):
        self._tests = tests
        return self

    def get_tests(self, value: SingleValue) -> Generator[MetricTestResult, None, None]:
        if self._tests is None:
            return None
        for test in self._tests:
            yield test(self, value)


class ByLabelMetric(Metric[ByLabelValue], ABC):
    _tests: Optional[typing.Dict[Label, List[SingleValueMetricTest]]]

    def label_metric(self, label: Label) -> SingleValueMetric:
        raise NotImplementedError()

    def with_tests(self, tests: Optional[typing.Dict[Label, List[SingleValueMetricTest]]]):
        self._tests = tests
        return self

    def get_tests(self, value: ByLabelValue) -> Generator[MetricTestResult, None, None]:
        if self._tests is None:
            return None
        for label, tests in self._tests.items():
            label_value = value.get_label_result(label)
            for test in tests:
                yield test(self, label_value)


class CountMetric(Metric[CountValue], ABC):
    _count_tests: Optional[List[SingleValueMetricTest]] = None
    _share_tests: Optional[List[SingleValueMetricTest]] = None

    def with_tests(
        self,
        count_tests: Optional[List[SingleValueMetricTest]] = None,
        share_tests: Optional[List[SingleValueMetricTest]] = None,
    ):
        self._count_tests = count_tests
        self._share_tests = share_tests
        return self

    def get_tests(self, value: CountValue) -> Generator[MetricTestResult, None, None]:
        if self._count_tests is None and self._share_tests is None:
            return None
        count_value = value.get_count()
        for test in self._count_tests or []:
            yield test(self, count_value)
        share_value = value.get_share()
        for test in self._share_tests or []:
            yield test(self, share_value)
