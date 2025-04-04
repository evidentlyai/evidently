import abc
from typing import Dict
from typing import Generic
from typing import List
from typing import Optional
from typing import TypeVar

import pandas as pd

from evidently.legacy.base_metric import GenericInputData
from evidently.legacy.base_metric import InputData
from evidently.legacy.base_metric import Metric
from evidently.legacy.calculation_engine.engine import Engine
from evidently.legacy.calculation_engine.engine import EngineDatasets
from evidently.legacy.calculation_engine.engine import TInputData
from evidently.legacy.calculation_engine.metric_implementation import MetricImplementation
from evidently.legacy.features.generated_features import FeatureResult
from evidently.legacy.features.generated_features import GeneratedFeatures
from evidently.legacy.options.base import Options
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.utils.data_preprocessing import DataDefinition
from evidently.legacy.utils.data_preprocessing import create_data_definition

TMetric = TypeVar("TMetric", bound=Metric)


class PythonEngine(Engine["PythonMetricImplementation", InputData, pd.DataFrame]):
    def convert_input_data(self, data: GenericInputData[pd.DataFrame]) -> InputData:
        if not isinstance(data.current_data, pd.DataFrame) or (
            data.reference_data is not None and not isinstance(data.reference_data, pd.DataFrame)
        ):
            raise ValueError("PandasEngine works only with pd.DataFrame input data")
        return InputData(
            data.reference_data,
            data.current_data,
            current_additional_features=None,
            reference_additional_features=None,
            column_mapping=data.column_mapping,
            data_definition=data.data_definition,
            additional_data=data.additional_data,
        )

    def get_data_definition(
        self,
        current_data,
        reference_data,
        column_mapping: ColumnMapping,
        categorical_features_cardinality: Optional[int] = None,
    ):
        if not isinstance(current_data, pd.DataFrame) or (
            reference_data is not None and not isinstance(reference_data, pd.DataFrame)
        ):
            raise ValueError("PandasEngine works only with pd.DataFrame input data")
        return create_data_definition(reference_data, current_data, column_mapping, categorical_features_cardinality)

    def calculate_additional_features(
        self, data: TInputData, features: List[GeneratedFeatures], options: Options
    ) -> Dict[GeneratedFeatures, FeatureResult[pd.DataFrame]]:
        result: Dict[GeneratedFeatures, FeatureResult[pd.DataFrame]] = {}
        for feature in features:
            current = feature.generate_features_renamed(data.current_data, data.data_definition, options)
            reference = (
                feature.generate_features_renamed(data.reference_data, data.data_definition, options)
                if data.reference_data is not None
                else None
            )

            result[feature] = FeatureResult(current, reference)
        return result

    def merge_additional_features(
        self, features: Dict[GeneratedFeatures, FeatureResult[pd.DataFrame]]
    ) -> EngineDatasets[pd.DataFrame]:
        currents = []
        references = []

        for feature, result in features.items():
            currents.append(result.current)
            if result.reference is not None:
                references.append(result.reference)

        if len(currents) == 0:
            current = None
        elif len(currents) == 1:
            current = currents[0]
        else:
            current = currents[0].join(currents[1:])  # type: ignore[arg-type]

        if len(references) == 0:
            return EngineDatasets(current=current, reference=None)
        if len(references) == 1:
            return EngineDatasets(current=current, reference=references[0])
        return EngineDatasets(current=current, reference=references[0].join(references[1:]))  # type: ignore[arg-type]

    def get_metric_implementation(self, metric):
        impl = super().get_metric_implementation(metric)
        if impl is None and isinstance(metric, Metric):

            class _Wrapper(PythonMetricImplementation):
                def calculate(self, context, data: InputData):
                    return self.metric.calculate(data)

            return _Wrapper(self, metric)
        return impl

    def form_datasets(
        self,
        data: Optional[InputData],
        features: List[GeneratedFeatures],
        data_definition: DataDefinition,
    ) -> EngineDatasets[pd.DataFrame]:
        if data is None:
            return EngineDatasets(current=None, reference=None)
        rename = {column.name: column.display_name for feature in features for column in feature.list_columns()}

        current = data.current_data
        if data.current_additional_features is not None:
            current = data.current_data.join(data.current_additional_features)

        current = current.rename(columns=rename)
        reference = data.reference_data
        if data.reference_data is not None and data.reference_additional_features is not None:
            reference = data.reference_data.join(data.reference_additional_features)

        if reference is not None:
            reference = reference.rename(columns=rename)

        return EngineDatasets(reference=reference, current=current)


class PythonMetricImplementation(Generic[TMetric], MetricImplementation):
    def __init__(self, engine: PythonEngine, metric: TMetric):
        self.engine = engine
        self.metric = metric

    @abc.abstractmethod
    def calculate(self, context, data: InputData):
        raise NotImplementedError

    @classmethod
    def supported_engines(cls):
        return (PythonEngine,)
