import abc
import logging
from typing import Dict
from typing import Generic
from typing import TypeVar
from typing import Union

import pandas as pd

from evidently.base_metric import ErrorResult
from evidently.base_metric import InputData
from evidently.base_metric import Metric
from evidently.base_metric import MetricResult
from evidently.calculation_engine.engine import Engine
from evidently.calculation_engine.metric_implementation import MetricImplementation


class PythonInputData(InputData):
    pass


TMetric = TypeVar("TMetric", bound=Metric)


class PythonEngine(Engine['PythonMetricImplementation', PythonInputData]):
    # def execute_metrics(self, context, data: InputData):
    #     calculations: Dict[Metric, Union[ErrorResult, MetricResult]] = {}
    #     converted_data = self.convert_input_data(data)
    #     for metric, calculation in self.get_metric_execution_iterator():
    #         if calculation not in calculations:
    #             logging.debug(f"Executing {type(calculation)}...")
    #             try:
    #                 calculations[metric] = calculation.calculate(context, converted_data)
    #             except BaseException as ex:
    #                 calculations[metric] = ErrorResult(exception=ex)
    #         else:
    #             logging.debug(f"Using cached result for {type(calculation)}")
    #         context.metric_results[metric] = calculations[metric]

    def convert_input_data(self, data: InputData) -> PythonInputData:
        if type(data.current_data) != pd.DataFrame or (
                data.reference_data is not None
                and type(data.reference_data) != pd.DataFrame):
            raise ValueError("PandasEngine works only with pd.DataFrame input data")
        return PythonInputData(
            data.reference_data,
            data.current_data,
            data.reference_additional_features,
            data.current_additional_features,
            data.column_mapping,
            data.data_definition,
        )

    def generate_additional_features(self, data: PythonInputData):
        curr_additional_data = None
        ref_additional_data = None
        features = {}
        for metric, calculation in self.get_metric_execution_iterator():
            try:
                required_features = metric.required_features(data.data_definition)
            except Exception as e:
                logging.error(f"failed to get features for {type(metric)}: {e}", exc_info=e)
                continue
            for feature in required_features:
                params = feature.get_parameters()
                if params is not None:
                    _id = (type(feature), params)
                    if _id in features:
                        continue
                    features[_id] = feature
                feature_data = feature.generate_feature(data.current_data, data.data_definition)
                feature_data.columns = [f"{feature.__class__.__name__}.{old}" for old in feature_data.columns]
                if curr_additional_data is None:
                    curr_additional_data = feature_data
                else:
                    curr_additional_data = curr_additional_data.join(feature_data)
                if data.reference_data is None:
                    continue
                ref_feature_data = feature.generate_feature(data.reference_data, data.data_definition)
                ref_feature_data.columns = [
                    f"{feature.__class__.__name__}.{old}" for old in ref_feature_data.columns
                ]

                if ref_additional_data is None:
                    ref_additional_data = ref_feature_data
                else:
                    ref_additional_data = ref_additional_data.join(ref_feature_data)
        data.current_additional_features = curr_additional_data
        data.reference_additional_features = ref_additional_data

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
        return (PythonEngine,)
