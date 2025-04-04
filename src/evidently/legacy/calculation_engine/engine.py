import abc
import dataclasses
import functools
import logging
from typing import TYPE_CHECKING
from typing import Dict
from typing import Generic
from typing import List
from typing import Optional
from typing import Tuple
from typing import Type
from typing import TypeVar
from typing import Union

from evidently.legacy.base_metric import ErrorResult
from evidently.legacy.base_metric import GenericInputData
from evidently.legacy.base_metric import Metric
from evidently.legacy.base_metric import MetricResult
from evidently.legacy.base_metric import TEngineDataType
from evidently.legacy.calculation_engine.metric_implementation import MetricImplementation
from evidently.legacy.features.generated_features import FeatureResult
from evidently.legacy.features.generated_features import GeneratedFeatures
from evidently.legacy.options.base import Options
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.utils.data_preprocessing import DataDefinition
from evidently.pydantic_utils import Fingerprint

if TYPE_CHECKING:
    from evidently.legacy.suite.base_suite import Context

TMetricImplementation = TypeVar("TMetricImplementation", bound=MetricImplementation)
TInputData = TypeVar("TInputData", bound=GenericInputData)


# EngineDatasets = Tuple[Optional[TEngineDataType], Optional[TEngineDataType]]


@dataclasses.dataclass
class EngineDatasets(Generic[TEngineDataType]):
    current: Optional[TEngineDataType]
    reference: Optional[TEngineDataType]

    def __iter__(self):
        yield self.current
        yield self.reference


class Engine(Generic[TMetricImplementation, TInputData, TEngineDataType]):
    def __init__(self):
        self.metrics = []
        self.tests = []

    def set_metrics(self, metrics):
        self.metrics = metrics

    def set_tests(self, tests):
        self.tests = tests

    def execute_metrics(self, context: "Context", data: GenericInputData):
        calculations: Dict[Metric, Union[ErrorResult, MetricResult]] = {}
        converted_data = self.convert_input_data(data)

        features_list = self.get_additional_features(converted_data.data_definition)
        features = self.calculate_additional_features(converted_data, features_list, context.options)
        context.set_features(features)
        self.inject_additional_features(converted_data, features)
        context.data = converted_data
        for metric, calculation in self.get_metric_execution_iterator():
            if calculation not in calculations:
                logging.debug(f"Executing {type(calculation)}...")
                try:
                    calculations[metric] = calculation.calculate(context, converted_data)
                except BaseException as ex:
                    calculations[metric] = ErrorResult(exception=ex)
            else:
                logging.debug(f"Using cached result for {type(calculation)}")
            context.metric_results[metric] = calculations[metric]

    @abc.abstractmethod
    def convert_input_data(self, data: GenericInputData) -> TInputData:
        raise NotImplementedError

    @abc.abstractmethod
    def get_data_definition(
        self,
        current_data: TEngineDataType,
        reference_data: TEngineDataType,
        column_mapping: ColumnMapping,
        categorical_features_cardinality: Optional[int] = None,
    ):
        raise NotImplementedError

    @abc.abstractmethod
    def calculate_additional_features(
        self, data: TInputData, features: List[GeneratedFeatures], options: Options
    ) -> Dict[GeneratedFeatures, FeatureResult[TEngineDataType]]:
        raise NotImplementedError

    @abc.abstractmethod
    def merge_additional_features(
        self, features: Dict[GeneratedFeatures, FeatureResult[TEngineDataType]]
    ) -> EngineDatasets[TEngineDataType]:
        raise NotImplementedError

    def inject_additional_features(self, data: TInputData, features: Dict[GeneratedFeatures, FeatureResult]):
        current, reference = self.merge_additional_features(features)
        data.current_additional_features = current
        data.reference_additional_features = reference

    def get_additional_features(self, data_definition: DataDefinition) -> List[GeneratedFeatures]:
        features: Dict[Fingerprint, GeneratedFeatures] = {}
        for metric, calculation in self.get_metric_execution_iterator():
            try:
                required_features: List[GeneratedFeatures] = metric.required_features(data_definition)
            except Exception as e:
                logging.error(f"failed to get features for {type(metric)}: {e}", exc_info=e)
                continue
            for feature in required_features:
                fp = feature.get_fingerprint()
                features[fp] = feature
        return list(features.values())

    def get_metric_implementation(self, metric):
        """
        Get engine specific metric implementation.
        """
        impl = _ImplRegistry.get(type(self), {}).get(type(metric))
        if impl is None:
            return None
        return impl(self, metric)

    def get_metric_execution_iterator(self) -> List[Tuple[Metric, TMetricImplementation]]:
        aggregated: Dict[Type[Metric], List[Metric]] = functools.reduce(_aggregate_metrics, self.metrics, {})
        metric_to_calculations = {}
        for metric_type, metrics in aggregated.items():
            metrics_by_parameters: Dict[tuple, List[Metric]] = functools.reduce(_aggregate_by_parameters, metrics, {})

            for metric in metrics:
                parameters = metric.get_parameters()
                if parameters is None:
                    metric_to_calculations[metric] = metric
                else:
                    metric_to_calculations[metric] = metrics_by_parameters[parameters][0]

        return [(metric, self.get_metric_implementation(metric_to_calculations[metric])) for metric in self.metrics]

    def form_datasets(
        self,
        data: Optional[TInputData],
        features: List[GeneratedFeatures],
        data_definition: DataDefinition,
    ) -> EngineDatasets[TEngineDataType]:
        raise NotImplementedError


def _aggregate_metrics(agg, item):
    agg[type(item)] = agg.get(type(item), []) + [item]
    return agg


def _aggregate_by_parameters(agg: dict, metric: Metric) -> dict:
    agg[metric.get_parameters()] = agg.get(metric.get_parameters(), []) + [metric]
    return agg


_ImplRegistry: Dict[Type, Dict[Type, Type]] = dict()


def metric_implementation(metric_cls):
    """
    Decorate metric implementation class, as a implementation for specific metric.
    """

    def wrapper(cls: Type[MetricImplementation]):
        _add_implementation(metric_cls, cls)
        return cls

    return wrapper


def _add_implementation(metric_cls, cls):
    engines = cls.supported_engines()
    for engine in engines:
        engine_impls = _ImplRegistry.get(engine, {})
        if metric_cls in engine_impls:
            raise ValueError(
                f"Multiple impls of metric {metric_cls}: {engine_impls[metric_cls]}"
                f" already set, but trying to set {cls}"
            )
        engine_impls[metric_cls] = cls
        _ImplRegistry[engine] = engine_impls
    return cls
