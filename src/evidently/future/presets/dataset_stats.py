from itertools import chain
from typing import Dict
from typing import List
from typing import Optional

from evidently import ColumnType
from evidently.future.container import MetricContainer
from evidently.future.metric_types import Metric
from evidently.future.metric_types import MetricId
from evidently.future.metric_types import MetricResult
from evidently.future.metrics import ColumnCount
from evidently.future.metrics import DuplicatedRowCount
from evidently.future.metrics import MaxValue
from evidently.future.metrics import MeanValue
from evidently.future.metrics import MinValue
from evidently.future.metrics import QuantileValue
from evidently.future.metrics import RowCount
from evidently.future.metrics import StdValue
from evidently.future.metrics.column_statistics import MissingValueCount
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


class ValueStats(MetricContainer):
    def __init__(self, column: str):
        self._column = column

    def generate_metrics(self, context: Context) -> List[Metric]:
        metrics: List[Metric] = [
            RowCount(),
            MissingValueCount(column=self._column),
        ]
        column_type = context.column(self._column).column_type
        if column_type == ColumnType.Numerical:
            metrics += [
                MinValue(column=self._column),
                MaxValue(column=self._column),
                MeanValue(column=self._column),
                StdValue(column=self._column),
                QuantileValue(column=self._column, quantile=0.25),
                QuantileValue(column=self._column, quantile=0.5),
                QuantileValue(column=self._column, quantile=0.75),
            ]
        if column_type == ColumnType.Categorical:
            metrics += []
        if column_type == ColumnType.Datetime:
            metrics += [
                MinValue(column=self._column),
                MaxValue(column=self._column),
            ]
        return metrics


class DatasetStats(MetricContainer):
    def generate_metrics(self, context: Context) -> List[Metric]:
        return [
            RowCount(),
            ColumnCount(),
            ColumnCount(column_type=ColumnType.Numerical),
            ColumnCount(column_type=ColumnType.Categorical),
            ColumnCount(column_type=ColumnType.Datetime),
            ColumnCount(column_type=ColumnType.Text),
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


class TextEvals(MetricContainer):
    def __init__(self, columns: Optional[List[str]] = None):
        self._columns = columns

    def generate_metrics(self, context: Context) -> List[Metric]:
        if self._columns is None:
            cols = context.data_definition.numerical_descriptors + context.data_definition.categorical_descriptors
        else:
            cols = self._columns
        metrics: List[Metric] = [RowCount()]
        metrics.extend(list(chain(*[ValueStats(column).metrics(context)[1:] for column in cols])))
        return metrics
