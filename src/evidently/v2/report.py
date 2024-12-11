from itertools import chain
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import TypeVar

from .datasets import Dataset
from .datasets import DatasetColumn
from .metrics.base import Metric
from .metrics.base import MetricId
from .metrics.base import MetricResult
from .metrics.base import render_widgets

TResultType = TypeVar("TResultType", bound="MetricResult")


class ContextColumnData:
    _column: DatasetColumn
    _labels: Optional[List[object]]

    def __init__(self, column: DatasetColumn):
        self._column = column
        self._labels = None

    def labels(self):
        if self._labels is None:
            self._labels = list(self._column.data.unique())
        return self._labels


class Context:
    _configuration: Optional["Report"]
    _metrics: Dict[MetricId, MetricResult]
    _metrics_graph: dict
    _data_columns: Dict[str, ContextColumnData]
    _input_data: Tuple[Dataset, Optional[Dataset]]
    _current_graph_level: dict

    def __init__(self):
        self._metrics = {}
        self._configuration = None
        self._data_columns = {}
        self._metrics_graph = {}
        self._current_graph_level = self._metrics_graph

    def init_dataset(self, current_data: Dataset, reference_data: Optional[Dataset]):
        self._input_data = (current_data, reference_data)
        self._data_columns = {
            column_name: ContextColumnData(current_data.column(column_name))
            for column_name, info in current_data._data_definition._columns.items()
        }

    def column(self, column_name: str) -> ContextColumnData:
        return self._data_columns[column_name]

    def calculate_metric(self, metric: Metric[TResultType]) -> TResultType:
        if metric.id not in self._current_graph_level:
            self._current_graph_level[metric.id] = {}
        prev_level = self._current_graph_level
        self._current_graph_level = prev_level[metric.id]
        if metric.id not in self._metrics:
            self._metrics[metric.id] = metric.call(*self._input_data)
        self._current_graph_level = prev_level
        return self._metrics[metric.id]


class Snapshot:
    _report: "Report"
    _context: Context  # stores report calculation progress

    def __init__(self, report: "Report"):
        self._report = report
        self._context = Context()

    def run(self, current_data: Dataset, reference_data: Optional[Dataset]):
        self._context.init_dataset(current_data, reference_data)
        for metric in self._report._metrics:
            self._context.calculate_metric(metric)

    def _repr_html_(self):
        return render_widgets(
            list(chain(*[self._context._metrics[metric].widget for metric in self._context._metrics_graph.keys()]))
        )


class Report:
    def __init__(self, metrics: List[Metric]):
        self._metrics = metrics

    def run(self, current_data: Dataset, reference_data: Optional[Dataset]) -> Snapshot:
        snapshot = Snapshot(self)
        snapshot.run(current_data, reference_data)
        return snapshot
