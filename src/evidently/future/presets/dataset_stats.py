from typing import Dict
from typing import List

from evidently import ColumnType
from evidently.future.metrics import ColumnCount
from evidently.future.metrics import DuplicatedRowCount
from evidently.future.metrics import Metric
from evidently.future.metrics import MetricContainer
from evidently.future.metrics import MetricResult
from evidently.future.metrics import RowCount
from evidently.future.metrics.base import MetricId
from evidently.future.metrics.dataset_statistics import AlmostConstantColumnsCount
from evidently.future.metrics.dataset_statistics import AlmostDuplicatedColumnsCount
from evidently.future.metrics.dataset_statistics import ConstantColumnsCount
from evidently.future.metrics.dataset_statistics import DatasetMissingValueCount
from evidently.future.metrics.dataset_statistics import DuplicatedColumnsCount
from evidently.future.metrics.dataset_statistics import EmptyColumnsCount
from evidently.future.metrics.dataset_statistics import EmptyRowsCount
from evidently.future.report import Context
from evidently.metrics import DatasetSummaryMetric
from evidently.model.widget import BaseWidgetInfo


class DatasetStats(MetricContainer):
    def generate_metrics(self, context: Context) -> List[Metric]:
        return [
            RowCount(),
            ColumnCount(),
            ColumnCount(ColumnType.Numerical),
            ColumnCount(ColumnType.Categorical),
            ColumnCount(ColumnType.Datetime),
            ColumnCount(ColumnType.Text),
            DuplicatedRowCount(),
            DuplicatedColumnsCount(),
            AlmostDuplicatedColumnsCount(),
            AlmostConstantColumnsCount(),
            EmptyRowsCount(),
            EmptyColumnsCount(),
            ConstantColumnsCount(),
            DatasetMissingValueCount(),
        ]

    def render(self, context: Context, results: Dict[MetricId, MetricResult]) -> List[BaseWidgetInfo]:
        metric = DatasetSummaryMetric()
        _, render = context.get_legacy_metric(metric)
        return render
