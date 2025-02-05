import abc
import dataclasses
import enum
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
from evidently.model.widget import AdditionalGraphInfo
from evidently.model.widget import BaseWidgetInfo
from evidently.pydantic_utils import EvidentlyBaseModel
from evidently.pydantic_utils import Fingerprint
from evidently.renderers.base_renderer import DetailsInfo
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
    _display_name: str = "<unset>"
    _metric: Optional["MetricCalculationBase"] = None
    _metric_value_location: Optional["MetricValueLocation"] = None
    _widget: Optional[List[BaseWidgetInfo]] = None
    _tests: Optional[Dict["BoundTest", "MetricTestResult"]] = None

    def set_tests(self, tests: Dict["BoundTest", "MetricTestResult"]):
        self._tests = tests

    def _repr_html_(self):
        assert self._widget
        widget = copy(self._widget)
        if self._tests:
            widget.append(metric_tests_widget(list(self.tests.values())))
        return render_results((self, None), html=False)

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

    def set_display_name(self, value: str):
        self._display_name = value

    def display_name(self) -> str:
        return self._display_name

    def to_dict(self):
        config = self.metric.to_metric().dict()
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
            "metric_id": f"{type}({','.join(config_items)})",
            "value": self.dict(),
        }

    @abc.abstractmethod
    def dict(self) -> object:
        raise NotImplementedError()

    @property
    def metric(self) -> "MetricCalculationBase":
        assert self._metric
        return self._metric

    @property
    def metric_value_location(self) -> "MetricValueLocation":
        assert self._metric_value_location
        return self._metric_value_location

    def __format__(self, format_spec):
        return str(self)


def render_widgets(widgets: List[BaseWidgetInfo]):
    items = []
    for info_item in widgets:
        for additional_graph in info_item.get_additional_graphs():
            if isinstance(additional_graph, AdditionalGraphInfo):
                items.append(DetailsInfo("", additional_graph.params, additional_graph.id))
            else:
                items.append(DetailsInfo("", additional_graph, additional_graph.id))
    additional_graphs = {
        f"{item.id}": dataclasses.asdict(item.info) if dataclasses.is_dataclass(item.info) else item.info
        for item in items
    }
    dashboard_id, dashboard_info = (
        "metric_" + str(uuid.uuid4()).replace("-", ""),
        DashboardInfo("Report", widgets=widgets),
    )
    template_params = TemplateParams(
        dashboard_id=dashboard_id,
        dashboard_info=dashboard_info,
        additional_graphs=additional_graphs,
    )
    return inline_iframe_html_template(template_params)


TMetricReturn = Tuple[MetricResult, Optional[MetricResult]]


def render_results(results: Union[TMetricReturn, List[TMetricReturn]], html=True):
    data = []
    if isinstance(results, tuple):
        data = [results]
    else:
        data = results
    widgets = list(itertools.chain(*[item[0].widget + [] if item[1] is None else item[1].widget for item in data]))
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

    def __format__(self, format_spec):
        return format(self.value, format_spec)


@dataclasses.dataclass
class ByLabelValue(MetricResult):
    values: Dict[Label, Value]

    def labels(self) -> List[Label]:
        return list(self.values.keys())

    def get_label_result(self, label: Label) -> SingleValue:
        value = SingleValue(self.values[label])
        metric = self.metric
        value._metric = metric
        if not isinstance(metric, ByLabelCalculation):
            raise ValueError(f"Metric {type(metric)} isn't ByLabelCalculation")
        value.set_display_name(metric.label_display_name(label))
        value._metric_value_location = ByLabelValueLocation(metric.to_metric(), label)
        return value

    def dict(self) -> object:
        return self.values


@dataclasses.dataclass
class CountValue(MetricResult):
    count: int
    share: float

    def get_count(self) -> SingleValue:
        value = SingleValue(self.count)
        metric = self.metric
        value._metric = metric
        if not isinstance(metric, CountCalculation):
            raise ValueError(f"Metric {type(metric)} is not Count")
        value.set_display_name(metric.count_display_name())
        value._metric_value_location = CountValueLocation(metric.to_metric(), True)
        return value

    def get_share(self) -> SingleValue:
        value = SingleValue(self.share)
        metric = self.metric
        value._metric = metric
        if not isinstance(metric, CountCalculation):
            raise ValueError(f"Metric {type(metric)} is not Count")
        value.set_display_name(metric.share_display_name())
        value._metric_value_location = CountValueLocation(metric.to_metric(), False)
        return value

    def dict(self) -> object:
        return {
            "count": self.count,
            "share": self.share,
        }

    def __format__(self, format_spec):
        return f"{format(self.count, format_spec)} ({format(self.share * 100, format_spec)}%)"


@dataclasses.dataclass
class MeanStdValue(MetricResult):
    mean: float
    std: float

    def get_mean(self) -> SingleValue:
        value = SingleValue(self.mean)
        metric = self.metric
        value._metric = metric
        if not isinstance(metric, MeanStdCalculation):
            raise ValueError(f"Metric {type(metric)} is not MeanStdCalculation")
        value.set_display_name(metric.mean_display_name())
        value._metric_value_location = MeanStdValueLocation(metric.to_metric(), True)
        return value

    def get_std(self) -> SingleValue:
        value = SingleValue(self.std)
        metric = self.metric
        if not isinstance(metric, MeanStdCalculation):
            raise ValueError(f"Metric {type(metric)} is not MeanStdCalculation")
        value._metric = metric
        value.set_display_name(metric.std_display_name())
        value._metric_value_location = MeanStdValueLocation(metric.to_metric(), False)
        return value

    def dict(self) -> object:
        return {
            "mean": self.mean,
            "std": self.std,
        }

    def __format__(self, format_spec):
        return f"{format(self.mean, format_spec)} (std: {format(self.std, format_spec)})"


class DatasetType(enum.Enum):
    Current = "current"
    Reference = "reference"


@dataclasses.dataclass
class MetricValueLocation:
    metric: "Metric"

    def value(self, context: "Context", dataset_type: DatasetType) -> SingleValue:
        value = self._metric_value_by_dataset(context, dataset_type)
        return self.extract_value(value)

    def _metric_value_by_dataset(self, context: "Context", dataset_type: DatasetType) -> MetricResult:
        if dataset_type == DatasetType.Current:
            return context.get_metric_result(self.metric.metric_id)
        if dataset_type == DatasetType.Reference:
            value = context.get_reference_metric_result(self.metric)
            return value
        raise ValueError(f"Unknown dataset type {dataset_type}")

    @abc.abstractmethod
    def extract_value(self, value: MetricResult) -> SingleValue:
        raise NotImplementedError()


@dataclasses.dataclass
class SingleValueLocation(MetricValueLocation):
    def extract_value(self, value: MetricResult) -> SingleValue:
        if not isinstance(value, SingleValue):
            raise ValueError(
                f"Unexpected type of metric result for metric[{str(value.metric)}]:"
                f" expected: {SingleValue.__name__}, actual: {type(value).__name__}"
            )
        return value


@dataclasses.dataclass
class ByLabelValueLocation(MetricValueLocation):
    label: Label

    def extract_value(self, value: MetricResult) -> SingleValue:
        if not isinstance(value, ByLabelValue):
            raise ValueError(
                f"Unexpected type of metric result for metric[{str(value.metric)}]:"
                f" expected: {ByLabelValue.__name__}, actual: {type(value).__name__}"
            )
        return value.get_label_result(self.label)


@dataclasses.dataclass
class CountValueLocation(MetricValueLocation):
    is_count: bool

    def extract_value(self, value: MetricResult) -> SingleValue:
        if not isinstance(value, CountValue):
            raise ValueError(
                f"Unexpected type of metric result for metric[{str(value.metric)}]:"
                f" expected: {CountValue.__name__}, actual: {type(value).__name__}"
            )
        return value.get_count() if self.is_count else value.get_share()


@dataclasses.dataclass
class MeanStdValueLocation(MetricValueLocation):
    is_mean: bool

    def extract_value(self, value: MetricResult) -> SingleValue:
        if not isinstance(value, MeanStdValue):
            raise ValueError(
                f"Unexpected type of metric result for metric[{str(value.metric)}]:"
                f" expected: {MeanStdValue.__name__}, actual: {type(value).__name__}"
            )
        return value.get_mean() if self.is_mean else value.get_std()


class MetricTestProto(Protocol[TResult]):
    def __call__(self, context: "Context", metric: "MetricCalculationBase", value: TResult) -> MetricTestResult: ...


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


def get_default_render_ref(title: str, result: MetricResult, ref_result: MetricResult) -> List[BaseWidgetInfo]:
    if isinstance(result, SingleValue):
        assert isinstance(ref_result, SingleValue)
        return [
            counter(
                title=title + " (current)",
                size=WidgetSize.HALF,
                counters=[CounterData(label="", value=f"{result.value:0.3f}")],
            ),
            counter(
                title=title + " (reference)",
                size=WidgetSize.HALF,
                counters=[CounterData(label="", value=f"{ref_result.value:0.3f}")],
            ),
        ]
    if isinstance(result, ByLabelValue):
        assert isinstance(ref_result, ByLabelValue)
        return [
            table_data(
                title=title,
                size=WidgetSize.FULL,
                column_names=["Label", "Current value", "Reference value"],
                data=[(k, f"{v:0.3f}", f"{ref_result.values[k]}") for k, v in result.values.items()],
            )
        ]
    if isinstance(result, CountValue):
        assert isinstance(ref_result, CountValue)
        return [
            counter(
                title=f"{title}: Current",
                size=WidgetSize.HALF,
                counters=[
                    CounterData(label="Count", value=str(result.count)),
                    CounterData(label="Share", value=f"{result.share:.2f}"),
                ],
            ),
            counter(
                title=f"{title}: Reference",
                size=WidgetSize.HALF,
                counters=[
                    CounterData(label="Count", value=str(ref_result.count)),
                    CounterData(label="Share", value=f"{ref_result.share:.2f}"),
                ],
            ),
        ]
    if isinstance(result, MeanStdValue):
        assert isinstance(ref_result, MeanStdValue)
        return [
            counter(
                title=f"{title}: Current",
                size=WidgetSize.HALF,
                counters=[
                    CounterData(label="Mean", value=f"{result.mean:.2f}"),
                    CounterData(label="Std", value=f"{result.std:.2f}"),
                ],
            ),
            counter(
                title=f"{title}: Reference",
                size=WidgetSize.HALF,
                counters=[
                    CounterData(label="Mean", value=f"{ref_result.mean:.2f}"),
                    CounterData(label="Std", value=f"{ref_result.std:.2f}"),
                ],
            ),
        ]
    raise NotImplementedError(f"No default render for {type(result)}")


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
                counters=[CounterData(label="", value=f"{result.mean:.2f}")],
            ),
            counter(
                title=f"{title}: std",
                size=WidgetSize.HALF,
                counters=[CounterData(label="", value=f"{result.std:.2f}")],
            ),
        ]
    raise NotImplementedError(f"No default render for {type(result)}")


TMetricResult = Union[TResult, Tuple[TResult, Optional[TResult]]]


class MetricCalculationBase(Generic[TResult]):
    """
    Base metric class.

    Metric is class to perform calculation over given dataset and return result.
    """

    _metric_id: MetricId

    def __init__(self, metric_id: MetricId) -> None:
        self._metric_id = metric_id

    def call(self, context: "Context") -> Tuple[TResult, Optional[TResult]]:
        """
        main method is used for executing metric
        Args:
            context:
        Returns:

        """
        result = self.calculate(context, *context._input_data)
        if isinstance(result, tuple):
            curr_result, ref_result = result
        else:
            curr_result, ref_result = result, None
        if not curr_result.is_widget_set():
            if ref_result is None:
                curr_result.widget = get_default_render(self.display_name(), curr_result)
            else:
                curr_result.widget = get_default_render_ref(self.display_name(), curr_result, ref_result)

        return curr_result, ref_result

    @abc.abstractmethod
    def calculate(self, context: "Context", current_data: Dataset, reference_data: Optional[Dataset]) -> TMetricResult:
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
    is_critical: bool = True

    @abstractmethod
    def to_test(self) -> MetricTestProto:
        raise not_implemented(self)

    def run(self, context: "Context", metric: "MetricCalculationBase", value: MetricResult) -> MetricTestResult:
        result: MetricTestResult = self.to_test()(context, metric, value)
        if result.status == TestStatus.FAIL and not self.is_critical:
            result.status = TestStatus.WARNING
        metric_conf = metric.to_metric()
        column = f" for {metric_conf.column}" if hasattr(metric_conf, "column") else ""
        result.description = f"{metric_conf.__class__.__name__}{column}: {result.description}"
        return result

    def bind_single(self, fingerprint: Fingerprint) -> "BoundTest":
        return SingleValueBoundTest(test=self, metric_fingerprint=fingerprint)

    def bind_count(self, fingerprint: Fingerprint, is_count: bool) -> "BoundTest":
        return CountBoundTest(test=self, metric_fingerprint=fingerprint, is_count=is_count)

    def bind_by_label(self, fingerprint: Fingerprint, label: Label):
        return ByLabelBoundTest(test=self, metric_fingerprint=fingerprint, label=label)

    def bind_mean_std(self, fingerprint: Fingerprint, is_mean: bool = True):
        return MeanStdBoundTest(test=self, metric_fingerprint=fingerprint, is_mean=is_mean)


class BoundTest(AutoAliasMixin, EvidentlyBaseModel, Generic[TResult], ABC):
    class Config:
        is_base_type = True

    __alias_type__: ClassVar[str] = "bound_test"
    test: MetricTest
    metric_fingerprint: Fingerprint

    @abstractmethod
    def run_test(self, context: "Context", calculation: MetricCalculationBase[TResult], metric_result: TResult):
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

    def _default_tests(self, context: "Context") -> List[BoundTest]:
        """
        allows to redefine default tests for metric
        Returns:
            list of tests to use as default
        """
        return []

    def _default_tests_with_reference(self, context: "Context") -> List[BoundTest]:
        """
        allows to redefine default tests for metric when calculated with reference
        Returns:
            list of tests to use as default when called with reference data
            None - if default tests should be returned
        """
        return []

    def _get_all_default_tests(self, context: "Context") -> List[BoundTest]:
        if context.has_reference:
            return self._default_tests_with_reference(context)
        return self._default_tests(context)

    def call(self, context: "Context"):
        return self.to_calculation().call(context)

    @abstractmethod
    def get_bound_tests(self, context: "Context") -> Sequence[BoundTest]:
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
            try:
                config_type = next(
                    b for b in typing_inspect.get_args(base) if isinstance(b, type) and issubclass(b, Metric)
                )
            except StopIteration:
                raise ValueError(f"Cannot find generic parameter of type Metric for {cls}")
            config_type.__calculation_type__ = cls
        super().__init_subclass__()

    def to_metric(self):
        return self.metric


TSingleValueMetricCalculation = TypeVar("TSingleValueMetricCalculation", bound="SingleValueCalculation")


class SingleValueBoundTest(BoundTest[SingleValue]):
    def run_test(
        self,
        context: "Context",
        calculation: MetricCalculationBase[SingleValue],
        metric_result: SingleValue,
    ) -> MetricTestResult:
        return self.test.run(context, calculation, metric_result)


class SingleValueMetric(Metric[TSingleValueMetricCalculation]):
    tests: Optional[List[MetricTest]] = None

    def get_bound_tests(self, context: "Context") -> List[BoundTest]:
        if self.tests is None and context.configuration.include_tests:
            return self._get_all_default_tests(context)
        fingerprint = self.get_fingerprint()
        return [t.bind_single(fingerprint) for t in (self.tests or [])]


TSingleValueMetric = TypeVar("TSingleValueMetric", bound=SingleValueMetric)


class SingleValueCalculation(MetricCalculation[SingleValue, TSingleValueMetric], Generic[TSingleValueMetric], ABC):
    pass


class ByLabelBoundTest(BoundTest[ByLabelValue]):
    label: Label

    def run_test(
        self,
        context: "Context",
        calculation: MetricCalculationBase,
        metric_result: ByLabelValue,
    ) -> MetricTestResult:
        value = metric_result.get_label_result(self.label)
        return self.test.run(context, calculation, value)


class ByLabelMetric(Metric["ByLabelCalculation"]):
    tests: Optional[Dict[Label, List[MetricTest]]] = None

    def get_bound_tests(self, context: "Context") -> List[BoundTest]:
        if self.tests is None and context.configuration.include_tests:
            return self._get_all_default_tests(context)
        fingerprint = self.get_fingerprint()
        return [t.bind_by_label(fingerprint, label=label) for label, tests in (self.tests or {}).items() for t in tests]


TByLabelMetric = TypeVar("TByLabelMetric", bound=ByLabelMetric)


class ByLabelCalculation(MetricCalculation[ByLabelValue, TByLabelMetric], Generic[TByLabelMetric], ABC):
    def label_metric(self, label: Label) -> SingleValueCalculation:
        raise NotImplementedError

    def label_display_name(self, label: Label) -> str:
        return self.display_name() + f" for label {label}"


class CountBoundTest(BoundTest[CountValue]):
    is_count: bool

    def run_test(
        self,
        context: "Context",
        calculation: MetricCalculationBase,
        metric_result: CountValue,
    ) -> MetricTestResult:
        return self.test.run(
            context,
            calculation,
            metric_result.get_count() if self.is_count else metric_result.get_share(),
        )


class CountMetric(Metric["CountCalculation"]):
    tests: Optional[List[MetricTest]] = None
    share_tests: Optional[List[MetricTest]] = None

    def get_bound_tests(self, context: "Context") -> Sequence[BoundTest]:
        if self.tests is None and self.share_tests is None and context.configuration.include_tests:
            return self._get_all_default_tests(context)
        fingerprint = self.get_fingerprint()
        return [t.bind_count(fingerprint, True) for t in (self.tests or [])] + [
            t.bind_count(fingerprint, False) for t in (self.share_tests or [])
        ]


TCountMetric = TypeVar("TCountMetric", bound=CountMetric)


class CountCalculation(MetricCalculation[CountValue, TCountMetric], Generic[TCountMetric], ABC):
    def count_display_name(self) -> str:
        return self.display_name()

    def share_display_name(self) -> str:
        return self.display_name()


class MeanStdBoundTest(BoundTest[MeanStdValue]):
    is_mean: bool

    def run_test(
        self,
        context: "Context",
        calculation: MetricCalculationBase,
        metric_result: MeanStdValue,
    ) -> MetricTestResult:
        return self.test.run(
            context,
            calculation,
            metric_result.get_mean() if self.is_mean else metric_result.get_std(),
        )


class MeanStdMetric(Metric["MeanStdCalculation"]):
    mean_tests: Optional[List[MetricTest]] = None
    std_tests: Optional[List[MetricTest]] = None

    def get_bound_tests(self, context: "Context") -> Sequence[BoundTest]:
        if self.mean_tests is None and self.mean_tests is None and context.configuration.include_tests:
            return self._get_all_default_tests(context)
        fingerprint = self.get_fingerprint()
        return [t.bind_mean_std(fingerprint, True) for t in (self.mean_tests or [])] + [
            t.bind_mean_std(fingerprint, False) for t in (self.std_tests or [])
        ]


TMeanStdMetric = TypeVar("TMeanStdMetric", bound=MeanStdMetric)


class MeanStdCalculation(MetricCalculation[MeanStdValue, TMeanStdMetric], Generic[TMeanStdMetric], ABC):
    def mean_display_name(self) -> str:
        return self.display_name()

    def std_display_name(self) -> str:
        return self.display_name()
