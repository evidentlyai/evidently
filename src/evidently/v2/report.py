import typing
from itertools import chain
from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import TypeVar
from typing import Union

from evidently.base_metric import Metric as LegacyMetric
from evidently.base_metric import MetricResult as LegacyMetricResult

from .. import ColumnMapping
from ..base_metric import InputData
from .datasets import Dataset
from .datasets import DatasetColumn
from .metrics import Metric
from .metrics import MetricContainer
from .metrics import MetricPreset
from .metrics import MetricResult
from .metrics.base import MetricId
from .metrics.base import metric_tests_widget
from .metrics.base import render_widgets

TResultType = TypeVar("TResultType", bound=MetricResult)
T = TypeVar("T", bound=LegacyMetricResult)


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
    _legacy_metrics: Dict[str, object]

    def __init__(self):
        self._metrics = {}
        self._metric_defs = {}
        self._configuration = None
        self._data_columns = {}
        self._metrics_graph = {}
        self._current_graph_level = self._metrics_graph
        self._legacy_metrics = {}

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
            self._current_graph_level[metric.id] = {"_self": metric}
        prev_level = self._current_graph_level
        self._current_graph_level = prev_level[metric.id]
        if metric.id not in self._metrics:
            self._metrics[metric.id] = metric.call(self)
        self._current_graph_level = prev_level
        return typing.cast(TResultType, self._metrics[metric.id])

    def get_metric_result(self, metric: Union[MetricId, Metric[TResultType]]) -> TResultType:
        if isinstance(metric, MetricId):
            return typing.cast(TResultType, self._metrics[metric])
        return self.calculate_metric(metric)

    def get_metric(self, metric: MetricId) -> Metric[TResultType]:
        return self._metrics_graph[metric]["_self"]

    def get_legacy_metric(self, metric: LegacyMetric[T]) -> T:
        fp = metric.get_fingerprint()
        if fp not in self._legacy_metrics:
            self._legacy_metrics[fp] = metric.calculate(
                InputData(
                    self._input_data[1].as_dataframe() if self._input_data[1] is not None else None,
                    self._input_data[0].as_dataframe(),
                    ColumnMapping(),
                    None,
                    {},
                    None,
                    None,
                )
            )
        return typing.cast(T, self._legacy_metrics[fp])


class Snapshot:
    _report: "Report"
    _context: Context  # stores report calculation progress

    def __init__(self, report: "Report"):
        self._report = report
        self._context = Context()

    @property
    def context(self) -> Context:
        return self._context

    @property
    def report(self) -> "Report":
        return self._report

    def run(self, current_data: Dataset, reference_data: Optional[Dataset]):
        self.context.init_dataset(current_data, reference_data)
        for item in self.report.items():
            if isinstance(item, (MetricPreset,)):
                metric_results = {}
                for metric in item.metrics():
                    metric_results[metric.id] = self.context.calculate_metric(metric)
            elif isinstance(item, (MetricContainer,)):
                for metric in item.metrics(self.context):
                    self.context.calculate_metric(metric)
            else:
                self.context.calculate_metric(item)

    def _repr_html_(self):
        from evidently.renderers.html_widgets import TabData
        from evidently.renderers.html_widgets import group_widget
        from evidently.renderers.html_widgets import widget_tabs

        results = [
            (
                metric,
                self._context.get_metric_result(metric).widget,
                self._context.get_metric_result(metric),
            )
            for metric in self.context._metrics_graph.keys()
        ]
        tabs = widget_tabs(
            title="",
            tabs=[
                TabData("Metrics", group_widget(title="", widgets=list(chain(*[result[1] for result in results])))),
                TabData("Tests", metric_tests_widget(list(chain(*[result[2].tests for result in results])))),
            ],
        )
        return render_widgets(
            [tabs],
        )


class Report:
    def __init__(self, metrics: List[Union[Metric, MetricPreset, MetricContainer]]):
        self._metrics = metrics

    def run(self, current_data: Dataset, reference_data: Optional[Dataset]) -> Snapshot:
        snapshot = Snapshot(self)
        snapshot.run(current_data, reference_data)
        return snapshot

    def items(self) -> Sequence[Union[Metric, MetricPreset, MetricContainer]]:
        return self._metrics
