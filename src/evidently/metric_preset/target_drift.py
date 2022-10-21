from typing import List
from typing import Sequence

from evidently.metric_preset.metric_preset import MetricPreset
from evidently.metrics import ColumnCorrelationsMetric
from evidently.metrics import ColumnDriftMetric
from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.utils.data_operations import DatasetColumns


class TargetDriftPreset(MetricPreset):
    def generate_metrics(self, data: InputData, columns: DatasetColumns) -> Sequence[Metric]:
        if columns.target_type is None:
            return []
        result: List[Metric] = []
        if columns.utility_columns.target is not None:
            result.append(ColumnDriftMetric(column_name=columns.utility_columns.target))
            result.append(ColumnCorrelationsMetric(column_name=columns.utility_columns.target))
        if columns.utility_columns.prediction is not None and isinstance(columns.utility_columns.prediction, str):
            result.append(ColumnDriftMetric(column_name=columns.utility_columns.prediction))
            result.append(ColumnCorrelationsMetric(column_name=columns.utility_columns.prediction))
        return result
