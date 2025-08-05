import abc
import enum
import inspect
import typing
import uuid
import warnings
from abc import ABC
from abc import abstractmethod
from copy import copy
from typing import TYPE_CHECKING
from typing import Any
from typing import Callable
from typing import ClassVar
from typing import Dict
from typing import Generic
from typing import List
from typing import Literal
from typing import Optional
from typing import Protocol
from typing import Sequence
from typing import Tuple
from typing import Type
from typing import TypeVar
from typing import Union

import numpy as np
import typing_inspect

from evidently._pydantic_compat import BaseModel
from evidently._pydantic_compat import Field
from evidently._pydantic_compat import parse_obj_as
from evidently._pydantic_compat import validator
from evidently.core.base_types import Label
from evidently.legacy.model.dashboard import DashboardInfo
from evidently.legacy.model.widget import AdditionalGraphInfo
from evidently.legacy.model.widget import BaseWidgetInfo
from evidently.legacy.renderers.base_renderer import DetailsInfo
from evidently.legacy.renderers.html_widgets import CounterData
from evidently.legacy.renderers.html_widgets import WidgetSize
from evidently.legacy.renderers.html_widgets import counter
from evidently.legacy.renderers.html_widgets import table_data
from evidently.legacy.tests.base_test import TestStatus
from evidently.legacy.utils.dashboard import TemplateParams
from evidently.legacy.utils.dashboard import file_html_template
from evidently.legacy.utils.dashboard import inline_iframe_html_template
from evidently.pydantic_utils import AutoAliasMixin
from evidently.pydantic_utils import EvidentlyBaseModel
from evidently.pydantic_utils import Fingerprint
from evidently.pydantic_utils import FrozenBaseModel
from evidently.pydantic_utils import PolymorphicModel

from ._utils import _flatten
from ._utils import not_implemented
from .datasets import Dataset
from .tests import GenericTest

if TYPE_CHECKING:
    from evidently.core.report import Context


MetricId = str


class MetricConfig(FrozenBaseModel):
    metric_id: MetricId
    params: Dict[str, Any]


class MetricValueLocation(BaseModel):
    metric: MetricConfig
    param: Dict[str, Any]

    def __init__(self, metric: MetricConfig, param: Dict[str, Any]):
        super().__init__(metric=metric, param=param)

    def params(self) -> Dict[str, Any]:
        return self.param

    def value(self, context: "Context", dataset_type: "DatasetType") -> "SingleValue":
        value = self._metric_value_by_dataset(context, dataset_type)
        return self.extract_value(value)

    def _metric_value_by_dataset(self, context: "Context", dataset_type: "DatasetType") -> "MetricResult":
        if dataset_type == DatasetType.Current:
            return context.get_metric_result(self.metric.metric_id)
        if dataset_type == DatasetType.Reference:
            value = context.get_reference_metric_result(self.metric.metric_id)
            return value
        raise ValueError(f"Unknown dataset type {dataset_type}")

    # @abc.abstractmethod
    def extract_value(self, value: "MetricResult") -> "SingleValue":
        if isinstance(value, SingleValue):
            return value
        if isinstance(value, ByLabelValue):
            label = self.params().get("label")
            if label is None or not isinstance(label, (bool, int, str)):
                raise ValueError("label parameter not set in metric location")
            result = value.get_label_result(label)
            if result is None:
                raise ValueError(f"label {label} does not exist in metric location")
            return result
        if isinstance(value, CountValue):
            value_type = self.params().get("value_type")
            if value_type not in ["count", "share"]:
                raise ValueError(f"Unknown value type {value_type}")
            return value.get_count() if self.params()["value_type"] == "count" else value.get_share()
        if isinstance(value, MeanStdValue):
            value_type = self.params().get("value_type")
            if value_type not in ["mean", "std"]:
                raise ValueError(f"Unknown value type {value_type}")
            return value.get_mean() if self.params()["value_type"] == "mean" else value.get_std()
        if isinstance(value, ByLabelCountValue):
            value_type = self.params().get("value_type")
            label = self.params().get("label")
            if label is None or not isinstance(label, (bool, int, str)):
                raise ValueError("label parameter not set in metric location")
            if value_type not in ["count", "share"]:
                raise ValueError(f"Unknown value type {value_type}")
            return value.counts[label] if self.params()["value_type"] == "count" else value.shares[label]
        raise ValueError(f"Unknown value type {type(value)}")


class MetricResult(AutoAliasMixin, PolymorphicModel):
    class Config:
        is_base_type = True

    __alias_type__: ClassVar[str] = "metric_result_v2"

    display_name: str
    metric_value_location: Optional["MetricValueLocation"] = None
    widget: Optional[List[BaseWidgetInfo]] = None
    tests: List["MetricTestResult"] = Field(default_factory=list)

    def set_tests(self, tests: List["MetricTestResult"]):
        self.tests = tests

    def _repr_html_(self):
        assert self.widget
        widget = copy(self.widget)
        if self.tests:
            widget.append(metric_tests_widget(list(self.tests)))
        return render_results((self, None), html=False)

    def is_widget_set(self) -> bool:
        return self.widget is not None

    def set_display_name(self, value: str):
        self.display_name = value

    @abc.abstractmethod
    def set_metric_location(self, metric: MetricConfig):
        raise NotImplementedError()

    def to_dict(self):
        return {
            "id": self.metric_value_location.metric.metric_id,
            "metric_id": self.explicit_metric_id(),
            "value": self.to_simple_dict(),
        }

    def explicit_metric_id(self):
        metric_value_location = self.metric_value_location
        config = metric_value_location.metric.params
        config_items = []
        type = None
        for field, value in config.items():
            if field.endswith("tests"):
                continue
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
        for key, value in self.metric_value_location.params().items():
            config_items.append(f"{key}={value}")
        return f"{type}({','.join(config_items)})"

    @abc.abstractmethod
    def to_simple_dict(self) -> object:
        raise NotImplementedError()

    def itervalues(self) -> typing.Iterable[Tuple[str, float]]:
        yield from _flatten(self.to_simple_dict())

    def get_widgets(self) -> List[BaseWidgetInfo]:
        return self.widget or []

    def get_metric_value_location(self) -> MetricValueLocation:
        assert self.metric_value_location, "Metric Value location should be set in all metric results"
        return self.metric_value_location

    def __format__(self, format_spec):
        return str(self)


def render_widgets(widgets: List[BaseWidgetInfo], as_iframe: bool = False):
    items = []
    for info_item in widgets:
        for additional_graph in info_item.get_additional_graphs():
            if isinstance(additional_graph, AdditionalGraphInfo):
                items.append(DetailsInfo(title="", info=additional_graph.params, id=additional_graph.id))
            else:
                items.append(DetailsInfo(title="", info=additional_graph, id=additional_graph.id))
    additional_graphs = {
        f"{item.id}": item.info.dict() if isinstance(item.info, BaseWidgetInfo) else item.info for item in items
    }
    dashboard_id, dashboard_info = (
        "metric_" + str(uuid.uuid4()).replace("-", ""),
        DashboardInfo(name="Report", widgets=widgets),
    )
    template_params = TemplateParams(
        dashboard_id=dashboard_id,
        dashboard_info=dashboard_info,
        additional_graphs=additional_graphs,
    )

    return inline_iframe_html_template(template_params) if as_iframe else file_html_template(template_params)


TMetricReturn = Tuple[MetricResult, Optional[MetricResult]]


def render_results(results: Union[TMetricReturn, List[TMetricReturn]], html=True):
    data = []
    if isinstance(results, tuple):
        data = [results]
    else:
        data = results
    widgets = []
    for item in data:
        if item[1] is None and item[0].widget is not None:
            widgets.extend(item[0].widget)
            continue
        if item[1] is not None and item[1].widget is not None:
            widgets.extend(item[1].widget)
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


class TestConfig(BaseModel):
    id: MetricTestId
    params: dict


class MetricTestResult(BaseModel):
    id: MetricTestId
    name: str
    description: str
    metric_config: MetricConfig
    test_config: dict
    status: TestStatus
    bound_test: Optional["BoundTest"] = None


class SingleValue(MetricResult):
    value: Value

    def to_simple_dict(self) -> object:
        return self.value

    def __format__(self, format_spec):
        return format(self.value, format_spec)

    def set_metric_location(self, metric: MetricConfig):
        self.metric_value_location = single_value_location(metric)


class ByLabelValue(MetricResult):
    class Config:
        smart_union = True

    values: Dict[Label, SingleValue]

    def labels(self) -> List[Label]:
        return list(self.values.keys())

    def get_label_result(self, label: Label) -> Optional[SingleValue]:
        value = self.values.get(
            label,
        )
        return value

    def set_metric_location(self, metric: MetricConfig):
        self.metric_value_location = single_value_location(metric)
        for k, v in self.values.items():
            v.metric_value_location = by_label_location(metric, k)

    def to_simple_dict(self) -> object:
        return {k: v.value for k, v in self.values.items()}

    @validator("values", pre=True)
    def convert_labels(cls, value):
        return {convert_types(k): v for k, v in value.items()}


class ByLabelCountValue(MetricResult):
    class Config:
        smart_union = True

    counts: Dict[Label, SingleValue]
    shares: Dict[Label, SingleValue]
    count_display_name_template: str = "Missing label {label} count"
    share_display_name_template: str = "Missing label {label} share"

    def labels(self) -> List[Label]:
        return list(self.counts.keys())

    @property
    def _metric_config(self) -> MetricConfig:
        try:
            val = next(iter(self.counts.values()))
        except StopIteration:
            raise ValueError("Empty dataset")
        return val.get_metric_value_location().metric

    def _missing_label_value(self, label: Label, is_count: bool) -> SingleValue:
        val = SingleValue(
            value=0,
            display_name=self.count_display_name_template.format(label=label)
            if is_count
            else self.share_display_name_template.format(label=label),
        )
        val.metric_value_location = by_label_count_value_location(self._metric_config, label, is_count=is_count)
        return val

    def get_label_result(self, label: Label) -> Tuple[SingleValue, SingleValue]:
        count = self.counts.get(
            label,
            self._missing_label_value(label, is_count=True),
        )
        share = self.shares.get(
            label,
            self._missing_label_value(label, is_count=False),
        )
        return count, share

    def to_simple_dict(self) -> object:
        return {
            "counts": {k: v.value for k, v in self.counts.items()},
            "shares": {k: v.value for k, v in self.shares.items()},
        }

    def set_metric_location(self, metric: MetricConfig):
        self.metric_value_location = single_value_location(metric)
        for k, v in self.counts.items():
            v.metric_value_location = by_label_count_value_location(metric, k, True)
        for k, v in self.shares.items():
            v.metric_value_location = by_label_count_value_location(metric, k, False)

    @validator("counts", "shares", pre=True)
    def convert_labels(cls, value):
        return {convert_types(k): v for k, v in value.items()}


try:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FutureWarning)
        np_bool = np.bool  # type: ignore[attr-defined]
except:  # noqa: E722
    np_bool = bool  # type: ignore[assignment]


try:
    np_bool_ = np.bool_
except:  # noqa: E722
    np_bool_ = bool  # type: ignore[assignment]


def convert_types(val):
    if isinstance(
        val,
        (
            np_bool,
            np_bool_,
            bool,
        ),
    ):
        return bool(val)
    if isinstance(val, (np.int16, np.int32, np.int64, int)):
        return int(val)
    if isinstance(val, str):
        return val
    if val is None or np.isnan(val):
        return val
    raise ValueError(f"type {type(val)} not supported as Label")


class CountValue(MetricResult):
    count: SingleValue
    share: SingleValue

    def get_count(self) -> SingleValue:
        return self.count

    def get_share(self) -> SingleValue:
        return self.share

    def to_simple_dict(self) -> object:
        return {
            "count": self.count.value,
            "share": self.share.value,
        }

    def set_metric_location(self, metric: MetricConfig):
        self.metric_value_location = single_value_location(metric)
        self.count.metric_value_location = count_value_location(metric, True)
        self.share.metric_value_location = count_value_location(metric, False)

    def __format__(self, format_spec):
        return f"{format(self.count, format_spec)} ({format(self.share.value * 100, format_spec)}%)"


class MeanStdValue(MetricResult):
    mean: SingleValue
    std: SingleValue

    def get_mean(self) -> SingleValue:
        return self.mean

    def get_std(self) -> SingleValue:
        return self.std

    def to_simple_dict(self) -> object:
        return {
            "mean": self.mean.value,
            "std": self.std.value,
        }

    def __format__(self, format_spec):
        return f"{format(self.mean, format_spec)} (std: {format(self.std, format_spec)})"

    def set_metric_location(self, metric: MetricConfig):
        self.metric_value_location = single_value_location(metric)
        self.mean.metric_value_location = mean_std_value_location(metric, True)
        self.std.metric_value_location = mean_std_value_location(metric, False)


class DatasetType(enum.Enum):
    Current = "current"
    Reference = "reference"


def single_value_location(metric: MetricConfig) -> MetricValueLocation:
    return MetricValueLocation(metric, {})


def by_label_location(metric: MetricConfig, label: Label) -> MetricValueLocation:
    return MetricValueLocation(metric, {"label": label})


ByLabelCountSlot = Union[Literal["count"], Literal["share"]]


def by_label_count_value_location(metric: MetricConfig, label: Label, is_count: bool) -> MetricValueLocation:
    return MetricValueLocation(metric, {"label": label, "value_type": "count" if is_count else "share"})


def count_value_location(metric: MetricConfig, is_count: bool) -> MetricValueLocation:
    return MetricValueLocation(metric, {"value_type": "count" if is_count else "share"})


def mean_std_value_location(metric: MetricConfig, is_mean: bool) -> MetricValueLocation:
    return MetricValueLocation(metric, {"value_type": "mean" if is_mean else "std"})


class MetricTestProto(Protocol[TResult]):
    def __call__(self, context: "Context", metric: "MetricCalculationBase", value: TResult) -> MetricTestResult: ...


SingleValueTest = MetricTestProto[SingleValue]


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
                data=sorted(
                    [(k, f"{v:0.3f}", f"{ref_result.values[k].value}") for k, v in result.values.items()],
                ),
            )
        ]
    if isinstance(result, ByLabelCountValue):
        assert isinstance(ref_result, ByLabelCountValue)
        return [
            table_data(
                title=title,
                size=WidgetSize.FULL,
                column_names=["Label", "Current value", "Reference value"],
                data=sorted(
                    [(k, f"{v:0.3f}", f"{ref_result.counts[k].value}") for k, v in result.counts.items()],
                ),
            )
        ]
    if isinstance(result, CountValue):
        assert isinstance(ref_result, CountValue)
        return [
            counter(
                title=f"{title}: Current",
                size=WidgetSize.HALF,
                counters=[
                    CounterData(label="Count", value=str(result.count.value)),
                    CounterData(label="Share", value=f"{result.share.value:.2f}"),
                ],
            ),
            counter(
                title=f"{title}: Reference",
                size=WidgetSize.HALF,
                counters=[
                    CounterData(label="Count", value=str(ref_result.count.value)),
                    CounterData(label="Share", value=f"{ref_result.share.value:.2f}"),
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
                    CounterData(label="Mean", value=f"{result.mean.value:.2f}"),
                    CounterData(label="Std", value=f"{result.std.value:.2f}"),
                ],
            ),
            counter(
                title=f"{title}: Reference",
                size=WidgetSize.HALF,
                counters=[
                    CounterData(label="Mean", value=f"{ref_result.mean.value:.2f}"),
                    CounterData(label="Std", value=f"{ref_result.std.value:.2f}"),
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
                data=sorted(
                    [(k, f"{v.value:0.3f}") for k, v in result.values.items()],
                ),
            )
        ]
    if isinstance(result, ByLabelCountValue):
        return [
            table_data(
                title=title,
                column_names=["Label", "Value"],
                data=sorted(
                    [(k, f"{v.value:0.3f}") for k, v in result.counts.items()],
                ),
            )
        ]
    if isinstance(result, CountValue):
        return [
            counter(
                title=f"{title}: count",
                size=WidgetSize.HALF,
                counters=[CounterData(label="", value=str(result.count.value))],
            ),
            counter(
                title=f"{title}: share",
                size=WidgetSize.HALF,
                counters=[CounterData(label="", value=f"{result.share.value:.2f}")],
            ),
        ]
    if isinstance(result, MeanStdValue):
        return [
            counter(
                title=f"{title}: mean",
                size=WidgetSize.HALF,
                counters=[CounterData(label="", value=f"{result.mean.value:.2f}")],
            ),
            counter(
                title=f"{title}: std",
                size=WidgetSize.HALF,
                counters=[CounterData(label="", value=f"{result.std.value:.2f}")],
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
    _replaced_display_name: Optional[str]

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

    def to_metric_config(self):
        return MetricConfig(
            metric_id=self.to_metric().metric_id,
            params=self.to_metric().dict(),
        )

    def group_by(self, group_by: Optional[str]) -> Union["MetricCalculationBase", List["MetricCalculationBase"]]:
        if group_by is None:
            return self
        raise not_implemented(self)


class MetricTest(AutoAliasMixin, EvidentlyBaseModel):
    class Config:
        is_base_type = True

    __alias_type__: ClassVar[str] = "test_v2"
    is_critical: bool = True
    alias: Optional[str] = None

    @abstractmethod
    def to_test(self) -> MetricTestProto:
        raise not_implemented(self)

    def run(self, context: "Context", metric: "MetricCalculationBase", value: MetricResult) -> MetricTestResult:
        result: MetricTestResult = self.to_test()(context, metric, value)
        status = result.status
        if result.status == TestStatus.FAIL and not self.is_critical:
            status = TestStatus.WARNING
        description = f"{self.alias or value.display_name}: {result.description}"
        return MetricTestResult(
            id=result.id,
            name=result.name,
            description=description,
            status=status,
            metric_config=result.metric_config,
            test_config=result.test_config,
        )

    def bind_single(self, fingerprint: Fingerprint) -> "BoundTest":
        return SingleValueBoundTest(test=self, metric_fingerprint=fingerprint)

    def bind_count(self, fingerprint: Fingerprint, is_count: bool) -> "BoundTest":
        return CountBoundTest(test=self, metric_fingerprint=fingerprint, is_count=is_count)

    def bind_by_label(self, fingerprint: Fingerprint, label: Label):
        return ByLabelBoundTest(test=self, metric_fingerprint=fingerprint, label=label)

    def bind_by_label_count(self, fingerprint: Fingerprint, label: Label, slot: ByLabelCountSlot):
        return ByLabelCountBoundTest(test=self, metric_fingerprint=fingerprint, label=label, slot=slot)

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


TCalculation = TypeVar("TCalculation")


class Metric(AutoAliasMixin, EvidentlyBaseModel, Generic[TCalculation]):
    __alias_type__: ClassVar[str] = "metric_v2"

    class Config:
        is_base_type = True
        smart_union = True

    __calculation_type__: ClassVar[Type]

    def __get_calculation_type__(self) -> Type[TCalculation]:
        if not hasattr(self, "__calculation_type__"):
            raise ValueError(f"{self.__class__.__name__} is not binded to Calculation type")
        if not issubclass(self.__calculation_type__, MetricCalculation):
            raise ValueError(f"{self.__class__.__name__} __calculation_type__ is not a subclass of MetricCalculation")
        return typing.cast(Type[TCalculation], self.__calculation_type__)

    def to_calculation(self) -> TCalculation:
        metric_type = self.__get_calculation_type__()
        if not issubclass(metric_type, MetricCalculation):
            raise ValueError(f"{self.__class__.__name__} __calculation_type__ is not a subclass of MetricCalculation")

        return typing.cast(TCalculation, metric_type(self.get_metric_id(), self))

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
        calculation = self.to_calculation()
        if not isinstance(calculation, MetricCalculation):
            raise ValueError(f"{self.__class__.__name__} __calculation_type__ is not a subclass of MetricCalculation")
        return calculation.call(context)

    @abstractmethod
    def get_bound_tests(self, context: "Context") -> Sequence[BoundTest]:
        raise not_implemented(self)


Render = List[BaseWidgetInfo]


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
        result = self.test.run(context, calculation, metric_result)
        result.bound_test = self
        return result


GenericTestList = Optional[List[Union[MetricTest, GenericTest]]]
SingleValueMetricTests = Optional[List[MetricTest]]
GenericSingleValueMetricTests = Union[GenericTestList, SingleValueMetricTests]


def convert_test(test: Union[MetricTest, GenericTest]) -> MetricTest:
    if isinstance(test, GenericTest):
        return test.for_metric()
    if isinstance(test, MetricTest):
        return test
    if isinstance(test, dict):
        return parse_obj_as(MetricTest, test)
    raise ValueError(f"test {test} is not a subclass of MetricTest")


def convert_tests(tests: Union[GenericSingleValueMetricTests, "GenericByLabelMetricTests", "MeanStdMetricTests"]):
    if isinstance(tests, dict):
        return {label: convert_tests(tests) for label, tests in tests.items()}
    if isinstance(tests, MeanStdMetricTests):
        return MeanStdMetricTests(mean=convert_tests(tests.mean), std=convert_tests(tests.std))
    return [convert_test(t) for t in tests] if tests is not None else None


class SingleValueMetric(Metric):
    tests: SingleValueMetricTests = None

    def get_bound_tests(self, context: "Context") -> List[BoundTest]:
        if self.tests is None and context.configuration.include_tests:
            return self._get_all_default_tests(context)
        fingerprint = self.get_fingerprint()
        return [t.bind_single(fingerprint) for t in (self.tests or [])]

    @validator("tests", pre=True)
    def validate_tests(cls, v):
        return convert_tests(v)


TSingleValueMetric = TypeVar("TSingleValueMetric", bound=SingleValueMetric)


class SingleValueCalculation(MetricCalculation[SingleValue, TSingleValueMetric], Generic[TSingleValueMetric], ABC):
    def result(self, value: Value) -> SingleValue:
        result = SingleValue(value=value, display_name=self.display_name())
        result.metric_value_location = single_value_location(self.to_metric_config())
        return result


class ByLabelBoundTest(BoundTest[ByLabelValue]):
    label: Label

    def run_test(
        self,
        context: "Context",
        calculation: MetricCalculationBase,
        metric_result: ByLabelValue,
    ) -> MetricTestResult:
        value = metric_result.get_label_result(self.label)
        if value is None:
            return MetricTestResult(
                id="",
                name="Missing label",
                description=f"Missing label {self.label} for {calculation.display_name()} test",
                metric_config=calculation.to_metric_config(),
                test_config=self.dict(),
                status=TestStatus.ERROR,
                bound_test=self,
            )
        result = self.test.run(context, calculation, value)
        result.bound_test = self
        return result


GenericTestDict = Optional[Dict[Label, List[Union[MetricTest, GenericTest]]]]
ByLabelMetricTests = Optional[Dict[Label, List[MetricTest]]]
GenericByLabelMetricTests = Union[GenericTestDict, ByLabelMetricTests]


class ByLabelMetric(Metric):
    tests: ByLabelMetricTests = None

    def get_bound_tests(self, context: "Context") -> List[BoundTest]:
        if self.tests is None and context.configuration.include_tests:
            return self._get_all_default_tests(context)
        fingerprint = self.get_fingerprint()
        return [t.bind_by_label(fingerprint, label=label) for label, tests in (self.tests or {}).items() for t in tests]

    @validator("tests", pre=True)
    def validate_tests(cls, val):
        return {k: convert_tests(v) for k, v in val.items()} if val is not None else None


TByLabelMetric = TypeVar("TByLabelMetric", bound=ByLabelMetric)
T = TypeVar("T")


class ByLabelCalculation(MetricCalculation[ByLabelValue, TByLabelMetric], Generic[TByLabelMetric], ABC):
    def label_metric(self, label: Label) -> SingleValueCalculation:
        raise NotImplementedError

    def label_display_name(self, label: Label) -> str:
        return self.display_name() + f" for label {label}"

    def _relabel(self, context: "Context", label: Label) -> Label:
        return label

    def result(self, values: Dict[Label, Value]) -> ByLabelValue:
        return ByLabelValue(
            values={
                k: SingleValue(
                    value=v,
                    display_name=self.label_display_name(k),
                    metric_value_location=by_label_location(self.to_metric_config(), k),
                )
                for k, v in values.items()
            },
            display_name=self.display_name(),
        )

    def collect_by_label_result(
        self,
        context: "Context",
        value_extract: Callable[[T], Value],
        current_result: Dict[Label, T],
        reference_result: Optional[Dict[Label, T]],
    ):
        return (
            self.result(
                {self._relabel(context, k): value_extract(v) for k, v in current_result.items()},
            ),
            None
            if reference_result is None
            else self.result(
                {self._relabel(context, k): value_extract(v) for k, v in reference_result.items()},
            ),
        )


class ByLabelCountBoundTest(BoundTest[ByLabelCountValue]):
    label: Label
    slot: ByLabelCountSlot

    def run_test(
        self,
        context: "Context",
        calculation: MetricCalculationBase,
        metric_result: ByLabelCountValue,
    ) -> MetricTestResult:
        value = metric_result.get_label_result(self.label)
        result = self.test.run(context, calculation, value[0] if self.slot == "count" else value[1])
        result.bound_test = self
        return result


class ByLabelCountMetric(Metric):
    replace_nan: Optional[Label] = None
    tests: Optional[Dict[Label, List[MetricTest]]] = None
    share_tests: Optional[Dict[Label, List[MetricTest]]] = None

    def get_bound_tests(self, context: "Context") -> List[BoundTest]:
        if self.tests is None and self.share_tests is None and context.configuration.include_tests:
            return self._get_all_default_tests(context)
        fingerprint = self.get_fingerprint()
        return [
            t.bind_by_label_count(fingerprint, label=label, slot="count")
            for label, tests in (self.tests or {}).items()
            for t in tests
        ] + [
            t.bind_by_label_count(fingerprint, label=label, slot="share")
            for label, tests in (self.share_tests or {}).items()
            for t in tests
        ]

    @validator("tests", "share_tests", pre=True)
    def validate_tests(cls, v):
        return convert_tests(v)


TByLabelCountMetric = TypeVar("TByLabelCountMetric", bound=ByLabelCountMetric)


class ByLabelCountCalculation(
    MetricCalculation[ByLabelCountValue, TByLabelCountMetric], Generic[TByLabelCountMetric], ABC
):
    def label_metric(self, label: Label) -> SingleValueCalculation:
        raise NotImplementedError

    def count_label_display_name(self, label: Label) -> str:
        raise NotImplementedError

    def share_label_display_name(self, label: Label) -> str:
        raise NotImplementedError

    def result(self, count: Dict[Label, Value], shares: Dict[Label, Value]) -> ByLabelCountValue:
        return ByLabelCountValue(
            counts={
                k: SingleValue(
                    value=v,
                    display_name=self.count_label_display_name(k),
                    metric_value_location=by_label_count_value_location(self.to_metric_config(), k, True),
                )
                for k, v in count.items()
            },
            shares={
                k: SingleValue(
                    value=v,
                    display_name=self.share_label_display_name(k),
                    metric_value_location=by_label_count_value_location(self.to_metric_config(), k, False),
                )
                for k, v in shares.items()
            },
            display_name=self.display_name(),
            count_display_name_template=self.count_label_display_name("{label}"),
            share_display_name_template=self.share_label_display_name("{label}"),
            metric_value_location=single_value_location(self.to_metric_config()),
        )


class CountBoundTest(BoundTest[CountValue]):
    is_count: bool

    def run_test(
        self,
        context: "Context",
        calculation: MetricCalculationBase,
        metric_result: CountValue,
    ) -> MetricTestResult:
        result = self.test.run(
            context,
            calculation,
            metric_result.get_count() if self.is_count else metric_result.get_share(),
        )
        result.bound_test = self
        return result


class CountMetric(Metric):
    tests: SingleValueMetricTests = None
    share_tests: SingleValueMetricTests = None

    def get_bound_tests(self, context: "Context") -> Sequence[BoundTest]:
        if self.tests is None and self.share_tests is None and context.configuration.include_tests:
            return self._get_all_default_tests(context)
        fingerprint = self.get_fingerprint()
        return [t.bind_count(fingerprint, True) for t in (self.tests or [])] + [
            t.bind_count(fingerprint, False) for t in (self.share_tests or [])
        ]

    @validator("tests", pre=True)
    def validate_tests(cls, v):
        return convert_tests(v)

    @validator("share_tests", pre=True)
    def validate_share_tests(cls, v):
        return convert_tests(v)


TCountMetric = TypeVar("TCountMetric", bound=CountMetric)


class CountCalculation(MetricCalculation[CountValue, TCountMetric], Generic[TCountMetric], ABC):
    def count_display_name(self) -> str:
        return self.display_name()

    def share_display_name(self) -> str:
        return self.display_name()

    def result(self, count: int, share: float) -> CountValue:
        return CountValue(
            count=SingleValue(
                value=count,
                display_name=self.count_display_name(),
                metric_value_location=count_value_location(self.to_metric_config(), True),
            ),
            share=SingleValue(
                value=share,
                display_name=self.share_display_name(),
                metric_value_location=count_value_location(self.to_metric_config(), False),
            ),
            display_name=self.display_name(),
        )


class MeanStdBoundTest(BoundTest[MeanStdValue]):
    is_mean: bool

    def run_test(
        self,
        context: "Context",
        calculation: MetricCalculationBase,
        metric_result: MeanStdValue,
    ) -> MetricTestResult:
        result = self.test.run(
            context,
            calculation,
            metric_result.get_mean() if self.is_mean else metric_result.get_std(),
        )
        result.bound_test = self
        return result


class MeanStdMetricTests(BaseModel):
    mean: SingleValueMetricTests = None
    std: SingleValueMetricTests = None

    def __init__(self, mean: GenericSingleValueMetricTests = None, std: GenericSingleValueMetricTests = None):
        super().__init__(mean=convert_tests(mean), std=convert_tests(std))


MeanStdMetricsPossibleTests = Union[MeanStdMetricTests, GenericSingleValueMetricTests, None]


def convert_to_mean_tests(tests: MeanStdMetricsPossibleTests) -> Optional[MeanStdMetricTests]:
    if tests is None:
        return None
    if isinstance(tests, MeanStdMetricTests):
        return tests
    if isinstance(tests, list):
        return MeanStdMetricTests(mean=tests)
    if isinstance(tests, dict):
        return parse_obj_as(MeanStdMetricTests, tests)
    raise ValueError(tests)


class MeanStdMetric(Metric):
    mean_tests: SingleValueMetricTests = None
    std_tests: SingleValueMetricTests = None

    def get_bound_tests(self, context: "Context") -> Sequence[BoundTest]:
        if self.mean_tests is None and self.mean_tests is None and context.configuration.include_tests:
            return self._get_all_default_tests(context)
        fingerprint = self.get_fingerprint()
        return [t.bind_mean_std(fingerprint, True) for t in (self.mean_tests or [])] + [
            t.bind_mean_std(fingerprint, False) for t in (self.std_tests or [])
        ]

    @validator("mean_tests", pre=True)
    def validate_mean_tests(cls, v):
        return convert_tests(v)

    @validator("std_tests", pre=True)
    def validate_std_tests(cls, v):
        return convert_tests(v)


TMeanStdMetric = TypeVar("TMeanStdMetric", bound=MeanStdMetric)


class MeanStdCalculation(MetricCalculation[MeanStdValue, TMeanStdMetric], Generic[TMeanStdMetric], ABC):
    def mean_display_name(self) -> str:
        return self.display_name()

    def std_display_name(self) -> str:
        return self.display_name()

    def result(self, mean: Value, std: Value) -> MeanStdValue:
        return MeanStdValue(
            mean=SingleValue(
                value=mean,
                display_name=self.mean_display_name(),
                metric_value_location=mean_std_value_location(self.to_metric_config(), True),
            ),
            std=SingleValue(
                value=std,
                display_name=self.std_display_name(),
                metric_value_location=mean_std_value_location(self.to_metric_config(), False),
            ),
            display_name=self.display_name(),
        )


class ColumnMetric(Metric, ABC):
    column: str


MetricTestResult.update_forward_refs()
