from typing import Dict
from typing import List

from evidently import ColumnType
from evidently.future.container import MetricContainer
from evidently.future.metric_types import Metric
from evidently.future.metric_types import MetricId
from evidently.future.metric_types import MetricResult
from evidently.future.metrics import ValueDrift
from evidently.future.metrics.column_statistics import DriftedColumnsCount
from evidently.future.report import Context
from evidently.metrics import DataDriftTable
from evidently.metrics import DatasetDriftMetric
from evidently.model.widget import BaseWidgetInfo


class DataDriftPreset(MetricContainer):
    def generate_metrics(self, context: Context) -> List[Metric]:
        types = [ColumnType.Numerical, ColumnType.Categorical, ColumnType.Text]
        return [
            DriftedColumnsCount(),
        ] + [ValueDrift(column=column) for column in context.data_definition.get_columns(types)]

    def render(self, context: Context, results: Dict[MetricId, MetricResult]) -> List[BaseWidgetInfo]:
        dataset_drift = context.get_legacy_metric(DatasetDriftMetric())[1]
        table = context.get_legacy_metric(DataDriftTable())[1]
        return dataset_drift + table
