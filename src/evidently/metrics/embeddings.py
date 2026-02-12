from typing import List
from typing import Optional

from evidently.core.metric_types import SingleValue
from evidently.core.metric_types import SingleValueCalculation
from evidently.core.metric_types import SingleValueMetric
from evidently.core.report import Context
from evidently.core.report import _default_input_data_generator
from evidently.legacy.base_metric import InputData
from evidently.legacy.metrics.data_drift.embedding_drift_methods import DistanceDriftMethod
from evidently.legacy.metrics.data_drift.embedding_drift_methods import DriftMethod
from evidently.legacy.metrics.data_drift.embedding_drift_methods import MMDDriftMethod
from evidently.legacy.metrics.data_drift.embedding_drift_methods import ModelDriftMethod
from evidently.legacy.metrics.data_drift.embedding_drift_methods import RatioDriftMethod
from evidently.legacy.metrics.data_drift.embeddings_drift import EmbeddingsDriftMetric
from evidently.legacy.metrics.data_drift.embeddings_drift import EmbeddingsDriftMetricResults
from evidently.legacy.model.widget import BaseWidgetInfo
from evidently.metrics._legacy import LegacyMetricCalculation


class EmbeddingsDrift(SingleValueMetric):
    embeddings_name: str
    drift_method: Optional[DriftMethod] = None


class EmbeddingsDriftCalculation(
    SingleValueCalculation[EmbeddingsDrift],
    LegacyMetricCalculation[SingleValue, EmbeddingsDrift, EmbeddingsDriftMetricResults, EmbeddingsDriftMetric],
):
    def _gen_input_data(self, context: "Context", task_name: Optional[str]) -> InputData:
        input_data = _default_input_data_generator(context, task_name)
        input_data.column_mapping.embeddings = context.data_definition.embeddings
        input_data.data_definition.embeddings = context.data_definition.embeddings
        return input_data

    def legacy_metric(self) -> EmbeddingsDriftMetric:
        return EmbeddingsDriftMetric(self.metric.embeddings_name, self.metric.drift_method)

    def calculate_value(
        self, context: "Context", legacy_result: EmbeddingsDriftMetricResults, render: List[BaseWidgetInfo]
    ) -> SingleValue:
        result = self.result(legacy_result.drift_score)
        result.widget = render
        return result

    def display_name(self) -> str:
        return f"Drift in embeddings: {self.metric.embeddings_name}"


__all__ = [
    "EmbeddingsDrift",
    "EmbeddingsDriftCalculation",
    "ModelDriftMethod",
    "DistanceDriftMethod",
    "RatioDriftMethod",
    "MMDDriftMethod",
]
