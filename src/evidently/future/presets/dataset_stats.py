from typing import Dict
from typing import List

from evidently import ColumnType
from evidently.future.metrics import ColumnCount
from evidently.future.metrics import Metric
from evidently.future.metrics import MetricContainer
from evidently.future.metrics import MetricResult
from evidently.future.metrics import RowCount
from evidently.future.metrics.base import MetricId
from evidently.future.report import Context
from evidently.metrics import DatasetSummaryMetric
from evidently.metrics.data_integrity.dataset_summary_metric import DatasetSummaryMetricRenderer
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
        ]

    def render(self, context: Context, results: Dict[MetricId, MetricResult]) -> List[BaseWidgetInfo]:
        metric = DatasetSummaryMetric()
        result = context.get_legacy_metric(metric)
        object.__setattr__(metric, "get_result", lambda: result)
        return DatasetSummaryMetricRenderer().render_html(metric)
