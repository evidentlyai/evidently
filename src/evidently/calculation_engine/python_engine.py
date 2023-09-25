import abc
import logging
from typing import Dict
from typing import Generic
from typing import TypeVar
from typing import Union

from evidently.base_metric import ErrorResult
from evidently.base_metric import InputData
from evidently.base_metric import Metric
from evidently.base_metric import MetricResult
from evidently.calculation_engine.engine import Engine
from evidently.calculation_engine.metric_implementation import MetricImplementation


class PythonInputData(InputData):
    pass


TMetric = TypeVar("TMetric", bound=Metric)


class PythonEngine(Engine['PythonMetricImplementation']):
    def execute_metrics(self, context, data):
        calculations: Dict[Metric, Union[ErrorResult, MetricResult]] = {}
        for metric, calculation in self.get_metric_execution_iterator():
            if calculation not in calculations:
                logging.debug(f"Executing {type(calculation)}...")
                try:
                    calculations[metric] = calculation.calculate(context, data)
                except BaseException as ex:
                    calculations[metric] = ErrorResult(exception=ex)
            else:
                logging.debug(f"Using cached result for {type(calculation)}")
            context.metric_results[metric] = calculations[metric]

    def get_metric_implementation(self, metric):
        impl = super().get_metric_implementation(metric)
        if impl is None and isinstance(metric, Metric):
            class _Wrapper(PythonMetricImplementation):
                def calculate(self, context, data: PythonInputData):
                    return self.metric.calculate(data)
            return _Wrapper(self, metric)
        return impl


class PythonMetricImplementation(Generic[TMetric], MetricImplementation):
    def __init__(self, engine: PythonEngine, metric: TMetric):
        self.engine = engine
        self.metric = metric

    @abc.abstractmethod
    def calculate(self, context, data: PythonInputData):
        raise NotImplementedError

    @classmethod
    def supported_engines(cls):
        return (PythonEngine, )
