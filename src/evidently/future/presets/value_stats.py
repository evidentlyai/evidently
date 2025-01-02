from typing import List

from evidently import ColumnType
from evidently.future.metrics import MaxValue
from evidently.future.metrics import MeanValue
from evidently.future.metrics import Metric
from evidently.future.metrics import MetricContainer
from evidently.future.metrics import MinValue
from evidently.future.metrics import QuantileValue
from evidently.future.metrics import RowCount
from evidently.future.metrics import StdValue
from evidently.future.metrics.column_statistics import MissingValueCount
from evidently.future.report import Context


class ValueStats(MetricContainer):
    def __init__(self, column: str):
        self._column = column

    def generate_metrics(self, context: Context) -> List[Metric]:
        metrics: List[Metric] = [
            RowCount(),
            MissingValueCount(self._column),
        ]
        column_type = context.column(self._column).column_type
        if column_type == ColumnType.Numerical:
            metrics += [
                MinValue(self._column),
                MaxValue(self._column),
                MeanValue(self._column),
                StdValue(self._column),
                QuantileValue(self._column, 0.25),
                QuantileValue(self._column, 0.5),
                QuantileValue(self._column, 0.75),
            ]
        if column_type == ColumnType.Categorical:
            metrics += []
        if column_type == ColumnType.Datetime:
            metrics += [
                MinValue(self._column),
                MaxValue(self._column),
            ]
        return metrics
