from datetime import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Type

from evidently.legacy.base_metric import GenericInputData
from evidently.legacy.calculation_engine.engine import Engine
from evidently.legacy.calculation_engine.engine import EngineDatasets
from evidently.legacy.calculation_engine.python_engine import PythonEngine
from evidently.legacy.features.generated_features import GeneratedFeatures
from evidently.legacy.options.base import AnyOptions
from evidently.legacy.options.base import Options
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.suite.base_suite import Runnable
from evidently.legacy.suite.base_suite import Suite


class FeatureGenerator(Runnable):
    _inner_suite: Suite

    def __init__(self, features: List[GeneratedFeatures], options: AnyOptions = None):
        self.features = features
        self.options = Options.from_any_options(options)
        self._inner_suite = Suite(self.options)

    def run(
        self,
        *,
        reference_data,
        current_data,
        column_mapping: Optional[ColumnMapping] = None,
        engine: Optional[Type[Engine]] = None,
        additional_data: Dict[str, Any] = None,
        timestamp: Optional[datetime] = None,
    ) -> None:
        if column_mapping is None:
            column_mapping = ColumnMapping()

        if current_data is None:
            raise ValueError("Current dataset should be present")

        self._inner_suite.reset()
        self._inner_suite.set_engine(PythonEngine() if engine is None else engine())

        context_engine = self._inner_suite.context.engine
        if context_engine is None:
            raise ValueError("No Engine is set")
        data_definition = self._inner_suite.context.get_data_definition(
            current_data,
            reference_data,
            column_mapping,
            self.options.data_definition_options.categorical_features_cardinality,
        )

        data = GenericInputData(
            reference_data=reference_data,
            current_data=current_data,
            column_mapping=column_mapping,
            data_definition=data_definition,
            additional_data=additional_data or {},
        )
        converted_data = context_engine.convert_input_data(data)
        result = context_engine.calculate_additional_features(
            converted_data, self.features, self._inner_suite.context.options
        )
        self._inner_suite.context.features = result

    def get_features(self, feature: Optional[GeneratedFeatures] = None) -> EngineDatasets[Any]:
        context = self._inner_suite.context
        if context.engine is None or context.features is None:
            raise ValueError("Call FeatureGenerator.run first")
        if feature is not None:
            result = context.features[feature]
            return EngineDatasets(result.current, result.reference)
        return context.engine.merge_additional_features(context.features)
