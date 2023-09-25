import abc
import functools
from typing import Dict
from typing import Generic
from typing import List
from typing import Tuple
from typing import Type
from typing import TypeVar

from evidently.base_metric import Metric
from evidently.calculation_engine.metric_implementation import MetricImplementation
from evidently.tests.base_test import Test

TMetricImplementation = TypeVar("TMetricImplementation", bound=MetricImplementation)


class Engine(Generic[TMetricImplementation]):
    def __init__(self, metrics, tests):
        self.metrics = metrics
        self.tests = tests

    @abc.abstractmethod
    def execute_metrics(self, context, data):
        raise NotImplementedError()

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

    def get_test_execution_iterator(self) -> List[Test]:
        return self.tests


def _aggregate_metrics(agg, item):
    agg[type(item)] = agg.get(type(item), []) + [item]
    return agg


def _aggregate_by_parameters(agg: dict, metric: Metric) -> dict:
    agg[metric.get_parameters()] = agg.get(metric.get_parameters(), []) + [metric]
    return agg


_ImplRegistry = dict()


def metric_implementation(metric_cls):
    def wrapper(cls: Type[MetricImplementation]):
        _add_implementation(metric_cls, cls)
        return cls
    return wrapper


def _add_implementation(metric_cls, cls):
    engines = cls.supported_engines()
    for engine in engines:
        engine_impls = _ImplRegistry.get(engine, {})
        if metric_cls in engine_impls:
            raise ValueError(f"Multiple impls of metric {metric_cls}: {engine_impls[metric_cls]}"
                             f" already set, but trying to set {cls}")
        engine_impls[metric_cls] = cls
        _ImplRegistry[engine] = engine_impls
    return cls