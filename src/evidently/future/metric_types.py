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

from evidently.future._utils import not_implemented
from evidently.future.datasets import Dataset
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

if typing.TYPE_CHECKING:
    from evidently.future.report import Context


class MetricResult:
    _metric: Optional["MetricCalculationBase"] = None
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

    @abc.abstractmethod
    def dict(self) -> object:
        raise NotImplementedError()


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

Value = Union[float, int]


@dataclasses.dataclass
class MetricTestResult:
    id: MetricTestId
    name: str
    description: str
    status: TestStatus

    def dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "status": self.status.value,
        }


@dataclasses.dataclass
class SingleValue(MetricResult):
    value: Value

    def dict(self) -> object:
        return self.value


@dataclasses.dataclass
class ByLabelValue(MetricResult):
    values: typing.Dict[Label, Value]

    def labels(self) -> List[Label]:
        return list(self.values.keys())

    def get_label_result(self, label: Label) -> SingleValue:
        value = self.values[label]
        return SingleValue(value)

    def dict(self) -> object:
        return self.values


@dataclasses.dataclass
class CountValue(MetricResult):
    count: int
    share: float

    def get_count(self) -> SingleValue:
        return SingleValue(self.count)

    def get_share(self) -> SingleValue:
        return SingleValue(self.share)

    def dict(self) -> object:
        return {
            "count": self.count,
            "share": self.share,
        }


@dataclasses.dataclass
class MeanStdValue(MetricResult):
    mean: float
    std: float

    def get_mean(self) -> SingleValue:
        return SingleValue(self.mean)

    def get_std(self) -> SingleValue:
        return SingleValue(self.std)

    def dict(self) -> object:
        return {
            "mean": self.mean,
            "std": self.std,
        }


class MetricTestProto(Protocol[TResult]):
    def __call__(self, metric: "MetricCalculationBase", value: TResult) -> MetricTestResult: ...


SingleValueTest = MetricTestProto[SingleValue]


MetricId = str

ByLabelValueTests = typing.Dict[Label, List[SingleValueTest]]


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
    if isinstance(result, MeanStdValue):
        return [
            counter(
                title=f"{title}: mean",
                size=WidgetSize.HALF,
                counters=[CounterData(label="", value=str(result.mean))],
            ),
            counter(
                title=f"{title}: std",
                size=WidgetSize.HALF,
                counters=[CounterData(label="", value=f"{result.std:.2f}")],
            ),
        ]
    raise NotImplementedError(f"No default render for {type(result)}")


class MetricCalculationBase(Generic[TResult]):
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
        try:
            result = self._call(context)
            if not result.is_widget_set():
                result.widget = get_default_render(self.display_name(), result)
            test_results = list(self.get_tests(result))
            if test_results and len(test_results) > 0:
                result.set_tests(test_results)
            return result
        except Exception as e:
            e.add_note(f"metric_type: {type(self).__name__}")
            raise

    def _call(self, context: "Context") -> TResult:
        return self.calculate(*context._input_data)

    @abc.abstractmethod
    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> TResult:
        raise not_implemented(self)

    @abstractmethod
    def get_tests(self, value: TResult) -> Generator[MetricTestResult, None, None]:
        raise not_implemented(self)

    @property
    def id(self) -> MetricId:
        return self._metric_id

    @abc.abstractmethod
    def display_name(self) -> str:
        raise not_implemented(self)

    @abc.abstractmethod
    def to_metric(self) -> "Metric":
        raise not_implemented(self)

    def group_by(self, group_by: Optional[str]) -> Union["MetricCalculationBase", List["MetricCalculationBase"]]:
        if group_by is None:
            return self
        raise not_implemented(self)


class AutoAliasMixin:
    __alias_type__: typing.ClassVar[str]

    @classmethod
    def __get_type__(cls):
        config = cls.__dict__.get("Config")
        if config is not None and config.__dict__.get("type_alias") is not None:
            return config.type_alias
        return f"evidently:{cls.__alias_type__}:{cls.__name__}"


TTest = TypeVar("TTest", bound=MetricTestProto)


class MetricTest(AutoAliasMixin, EvidentlyBaseModel, Generic[TTest]):
    class Config:
        is_base_type = True

    __alias_type__: typing.ClassVar[str] = "test_config"

    @abstractmethod
    def to_test(self) -> TTest:
        raise not_implemented(self)


TCalculation = TypeVar("TCalculation", bound="MetricCalculation")


class Metric(AutoAliasMixin, EvidentlyBaseModel, Generic[TCalculation]):
    __alias_type__: typing.ClassVar[str] = "metric_v2"

    class Config:
        is_base_type = True

    __calculation_type__: typing.ClassVar[typing.Type[TCalculation]]

    def __get_calculation_type__(self) -> typing.Type[TCalculation]:
        if not hasattr(self, "__calculation_type__"):
            raise ValueError(f"{self.__class__.__name__} is not binded to Calculation type")
        return self.__calculation_type__

    def to_calculation(self) -> TCalculation:
        metric_type = self.__get_calculation_type__()
        return metric_type(self.get_metric_id(), self)

    def get_metric_id(self) -> str:
        return self.get_fingerprint()

    @property
    def metric_id(self) -> str:
        return self.get_fingerprint()

    def _default_tests(self) -> List[MetricTestProto[TResult]]:
        """
        allows to redefine default tests for metric
        Returns:
            list of tests to use as default
        """
        return []

    def _default_tests_with_reference(self) -> Optional[List[MetricTestProto[TResult]]]:
        """
        allows to redefine default tests for metric when calculated with reference
        Returns:
            list of tests to use as default when called with reference data
            None - if default tests should be returned
        """
        return None

    def call(self, context: "Context"):
        return self.to_calculation().call(context)


Render = List[BaseWidgetInfo]


@dataclasses.dataclass
class MetricResultValue:
    metric: Metric
    attributes: typing.Dict[str, str]
    value: Value
    render: Render


TMetric = TypeVar("TMetric", bound=Metric)


class MetricCalculation(MetricCalculationBase[TResult], Generic[TResult, TMetric], abc.ABC):
    def __init__(self, metric_id: MetricId, metric: TMetric):
        self.metric = metric
        super().__init__(metric_id)

    def __init_subclass__(cls):
        if not inspect.isabstract(cls) and ABC not in cls.__bases__:
            base = typing_inspect.get_generic_bases(cls)[0]  # fixme only works for simple cases
            # print(base, typing_inspect.get_args(base))
            config_type = typing_inspect.get_args(base)[-1]
            if not isinstance(config_type, type) or not issubclass(config_type, Metric):
                raise ValueError(f"Value of generic parameter TMetric for {config_type} should be Metric subclass")
            config_type.__calculation_type__ = cls
        super().__init_subclass__()

    def to_metric(self):
        return self.metric


TSingleValueMetricCalculation = TypeVar("TSingleValueMetricCalculation", bound="SingleValueCalculation")


class SingleValueMetric(Metric[TSingleValueMetricCalculation]):
    tests: List[MetricTest[SingleValue]] = []


TSingleValueMetric = TypeVar("TSingleValueMetric", bound=SingleValueMetric)


class SingleValueCalculation(MetricCalculation[SingleValue, TSingleValueMetric], Generic[TSingleValueMetric], ABC):
    def get_tests(self, value: SingleValue) -> Generator[MetricTestResult, None, None]:
        yield from (t.to_test()(self, value) for t in self.metric.tests)


class ByLabelMetric(Metric["ByLabelCalculation"]):
    tests: typing.Dict[Label, List[MetricTest[SingleValue]]] = {}


TByLabelMetric = TypeVar("TByLabelMetric", bound=ByLabelMetric)


class ByLabelCalculation(MetricCalculation[ByLabelValue, TByLabelMetric], Generic[TByLabelMetric], ABC):
    def label_metric(self, label: Label) -> SingleValueCalculation:
        raise NotImplementedError()

    def get_tests(self, value: ByLabelValue) -> Generator[MetricTestResult, None, None]:
        for label, tests in self.metric.tests.items():
            label_value = value.get_label_result(label)
            for test in tests:
                yield test.to_test()(self, label_value)


class CountMetric(Metric["CountCalculation"]):
    count_tests: List[MetricTest[SingleValue]] = []
    share_tests: List[MetricTest[SingleValue]] = []


TCountMetric = TypeVar("TCountMetric", bound=CountMetric)


class CountCalculation(MetricCalculation[CountValue, TCountMetric], Generic[TCountMetric], ABC):
    def get_tests(self, value: CountValue) -> Generator[MetricTestResult, None, None]:
        # todo: do not call to_metric here
        yield from (t.to_test()(self, value.get_count()) for t in self.metric.count_tests)
        yield from (t.to_test()(self, value.get_share()) for t in self.metric.share_tests)


class MeanStdMetric(Metric["MeanStdCalculation"]):
    mean_tests: List[MetricTest[SingleValue]] = []
    std_tests: List[MetricTest[SingleValue]] = []


TMeanStdMetric = TypeVar("TMeanStdMetric", bound=MeanStdMetric)


class MeanStdCalculation(MetricCalculation[MeanStdValue, TMeanStdMetric], Generic[TMeanStdMetric], ABC):
    def get_tests(self, value: MeanStdValue) -> Generator[MetricTestResult, None, None]:
        # todo: do not call to_metric here
        yield from (t.to_test()(self, value.get_mean()) for t in self.metric.mean_tests)
        yield from (t.to_test()(self, value.get_std()) for t in self.metric.std_tests)
