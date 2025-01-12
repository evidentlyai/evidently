import abc
import dataclasses
import inspect
import itertools
import uuid
from abc import ABC
from abc import abstractmethod
from copy import copy
from typing import TYPE_CHECKING
from typing import ClassVar
from typing import Dict
from typing import Generic
from typing import List
from typing import Optional
from typing import Protocol
from typing import Sequence
from typing import Tuple
from typing import Type
from typing import TypeVar
from typing import Union

import typing_inspect

from evidently.future._utils import not_implemented
from evidently.future.datasets import Dataset
from evidently.metric_results import Label
from evidently.model.dashboard import DashboardInfo
from evidently.model.widget import BaseWidgetInfo
from evidently.pydantic_utils import EvidentlyBaseModel
from evidently.pydantic_utils import Fingerprint
from evidently.renderers.html_widgets import CounterData
from evidently.renderers.html_widgets import WidgetSize
from evidently.renderers.html_widgets import counter
from evidently.renderers.html_widgets import table_data
from evidently.tests.base_test import TestStatus
from evidently.utils.dashboard import TemplateParams
from evidently.utils.dashboard import inline_iframe_html_template

if TYPE_CHECKING:
    from evidently.future.report import Context


class MetricResult:
    _metric: Optional["MetricCalculationBase"] = None
    _widget: Optional[List[BaseWidgetInfo]] = None
    _tests: Optional[Dict["BoundTest", "MetricTestResult"]] = None

    def set_tests(self, tests: Dict["BoundTest", "MetricTestResult"]):
        self._tests = tests

    def _repr_html_(self):
        assert self._widget
        widget = copy(self._widget)
        if self._tests:
            widget.append(metric_tests_widget(list(self.tests.values())))
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
    def tests(self) -> Dict["BoundTest", "MetricTestResult"]:
        return self._tests or {}

    def to_dict(self):
        config = self._metric.metric.dict()  # type: ignore[attr-defined]
        config_items = []
        type = None
        for field, value in config.items():
            if field == "type":
                type = value.split(":")[-1]
                continue
            elif value is None:
                continue
            elif isinstance(value, list):
                if len(value) > 0:
                    config_items.append(f"{field}={','.join(str(x) for x in value)}")
                continue
            elif isinstance(value, dict):
                continue
            else:
                config_items.append(f"{field}={str(value)}")
        return {
            "id": self._metric.id,
            "metric_id": f"{type}({",".join(config_items)})",
            "value": self.dict(),
        }

    @abc.abstractmethod
    def dict(self) -> object:
        raise NotImplementedError()


def render_widgets(widgets: List[BaseWidgetInfo]):
    dashboard_id, dashboard_info = (
        "metric_" + str(uuid.uuid4()).replace("-", ""),
        DashboardInfo("Report", widgets=widgets),
    )
    template_params = TemplateParams(
        dashboard_id=dashboard_id,
        dashboard_info=dashboard_info,
        additional_graphs={},
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
    values: Dict[Label, Value]

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

ByLabelValueTests = Dict[Label, List[SingleValueTest]]


def metric_tests_widget(tests: List[MetricTestResult]) -> BaseWidgetInfo:
    return BaseWidgetInfo(
        title="",
        size=2,
        type="test_suite",
        params={
            "v2_test": True,
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
                counters=[CounterData(label="", value=f"{result.value:0.3f}")],
            ),
        ]
    if isinstance(result, ByLabelValue):
        return [
            table_data(
                title=title,
                column_names=["Label", "Value"],
                data=[(k, f"{v:0.3f}") for k, v in result.values.items()],
            )
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
        result = self._call(context)
        if not result.is_widget_set():
            result.widget = get_default_render(self.display_name(), result)
        test_results = {tc: tc.run_test(self, result) for tc in self.to_metric().get_bound_tests()}
        if test_results and len(test_results) > 0:
            result.set_tests(test_results)
        return result

    def _call(self, context: "Context") -> TResult:
        return self.calculate(*context._input_data)

    @abc.abstractmethod
    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> TResult:
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
    __alias_type__: ClassVar[str]

    @classmethod
    def __get_type__(cls):
        config = cls.__dict__.get("Config")
        if config is not None and config.__dict__.get("type_alias") is not None:
            return config.type_alias
        return f"evidently:{cls.__alias_type__}:{cls.__name__}"


class MetricTest(AutoAliasMixin, EvidentlyBaseModel):
    class Config:
        is_base_type = True

    __alias_type__: ClassVar[str] = "test_v2"

    @abstractmethod
    def to_test(self) -> MetricTestProto:
        raise not_implemented(self)


class BoundTest(AutoAliasMixin, EvidentlyBaseModel, Generic[TResult], ABC):
    class Config:
        is_base_type = True

    __alias_type__: ClassVar[str] = "bound_test"
    test: MetricTest
    metric_fingerprint: Fingerprint

    @abstractmethod
    def run_test(self, calculation: MetricCalculationBase[TResult], metric_result: TResult):
        raise NotImplementedError(self.__class__)


TCalculation = TypeVar("TCalculation", bound="MetricCalculation")


class Metric(AutoAliasMixin, EvidentlyBaseModel, Generic[TCalculation]):
    __alias_type__: ClassVar[str] = "metric_v2"

    class Config:
        is_base_type = True

    __calculation_type__: ClassVar[Type[TCalculation]]

    def __get_calculation_type__(self) -> Type[TCalculation]:
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

    @abstractmethod
    def get_bound_tests(self) -> Sequence[BoundTest]:
        raise not_implemented(self)


Render = List[BaseWidgetInfo]


@dataclasses.dataclass
class MetricResultValue:
    metric: Metric
    attributes: Dict[str, str]
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


class SingleValueBoundTest(BoundTest[SingleValue]):
    def run_test(self, calculation: MetricCalculationBase[SingleValue], metric_result: SingleValue) -> MetricTestResult:
        return self.test.to_test()(calculation, metric_result)


class SingleValueMetric(Metric[TSingleValueMetricCalculation]):
    tests: List[MetricTest] = []

    def get_bound_tests(self) -> List[BoundTest]:
        return [SingleValueBoundTest(test=t, metric_fingerprint=self.get_fingerprint()) for t in self.tests]


TSingleValueMetric = TypeVar("TSingleValueMetric", bound=SingleValueMetric)


class SingleValueCalculation(MetricCalculation[SingleValue, TSingleValueMetric], Generic[TSingleValueMetric], ABC):
    pass


class ByLabelBoundTest(BoundTest[ByLabelValue]):
    label: Label

    def run_test(self, calculation: MetricCalculationBase, metric_result: ByLabelValue) -> MetricTestResult:
        value = metric_result.get_label_result(self.label)
        return self.test.to_test()(calculation, value)


class ByLabelMetric(Metric["ByLabelCalculation"]):
    tests: Dict[Label, List[MetricTest]] = {}

    def get_bound_tests(self) -> List[BoundTest]:
        return [
            ByLabelBoundTest(test=t, label=label, metric_fingerprint=self.get_fingerprint())
            for label, tests in self.tests.items()
            for t in tests
        ]


TByLabelMetric = TypeVar("TByLabelMetric", bound=ByLabelMetric)


class ByLabelCalculation(MetricCalculation[ByLabelValue, TByLabelMetric], Generic[TByLabelMetric], ABC):
    def label_metric(self, label: Label) -> SingleValueCalculation:
        raise NotImplementedError


class CountBoundTest(BoundTest[CountValue]):
    is_count: bool

    def run_test(self, calculation: MetricCalculationBase, metric_result: CountValue) -> MetricTestResult:
        return self.test.to_test()(
            calculation, metric_result.get_count() if self.is_count else metric_result.get_share()
        )


class CountMetric(Metric["CountCalculation"]):
    count_tests: List[MetricTest] = []
    share_tests: List[MetricTest] = []

    def get_bound_tests(self) -> Sequence[BoundTest]:
        return [
            CountBoundTest(is_count=True, test=t, metric_fingerprint=self.get_fingerprint()) for t in self.count_tests
        ] + [
            CountBoundTest(is_count=False, test=t, metric_fingerprint=self.get_fingerprint()) for t in self.share_tests
        ]


TCountMetric = TypeVar("TCountMetric", bound=CountMetric)


class CountCalculation(MetricCalculation[CountValue, TCountMetric], Generic[TCountMetric], ABC):
    pass


class MeanStdBoundTest(BoundTest[MeanStdValue]):
    is_mean: bool

    def run_test(self, calculation: MetricCalculationBase, metric_result: MeanStdValue) -> MetricTestResult:
        return self.test.to_test()(calculation, metric_result.get_mean() if self.is_mean else metric_result.get_std())


class MeanStdMetric(Metric["MeanStdCalculation"]):
    mean_tests: List[MetricTest] = []
    std_tests: List[MetricTest] = []

    def get_bound_tests(self) -> Sequence[BoundTest]:
        return [
            MeanStdBoundTest(is_mean=True, test=t, metric_fingerprint=self.get_fingerprint()) for t in self.mean_tests
        ] + [
            MeanStdBoundTest(is_mean=False, test=t, metric_fingerprint=self.get_fingerprint()) for t in self.mean_tests
        ]


TMeanStdMetric = TypeVar("TMeanStdMetric", bound=MeanStdMetric)


class MeanStdCalculation(MetricCalculation[MeanStdValue, TMeanStdMetric], Generic[TMeanStdMetric], ABC):
    pass
