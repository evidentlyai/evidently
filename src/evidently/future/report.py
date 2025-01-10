import json
import typing
from datetime import datetime
from itertools import chain
from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import TypeVar
from typing import Union

from evidently import ColumnMapping
from evidently import ColumnType
from evidently.base_metric import InputData
from evidently.base_metric import Metric as LegacyMetric
from evidently.base_metric import MetricResult as LegacyMetricResult
from evidently.future.container import MetricContainer
from evidently.future.datasets import BinaryClassification
from evidently.future.datasets import DataDefinition
from evidently.future.datasets import Dataset
from evidently.future.datasets import DatasetColumn
from evidently.future.metric_types import Metric
from evidently.future.metric_types import MetricCalculationBase
from evidently.future.metric_types import MetricId
from evidently.future.metric_types import MetricResult
from evidently.future.metric_types import metric_tests_widget
from evidently.future.metric_types import render_widgets
from evidently.future.preset_types import MetricPreset
from evidently.model.widget import BaseWidgetInfo
from evidently.renderers.base_renderer import DEFAULT_RENDERERS
from evidently.suite.base_suite import MetadataValueType
from evidently.suite.base_suite import _discover_dependencies
from evidently.suite.base_suite import find_metric_renderer
from evidently.utils import NumpyEncoder

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

    @property
    def column_type(self) -> ColumnType:
        return self._column.type


class Context:
    _configuration: Optional["Report"]
    _metrics: Dict[MetricId, MetricResult]
    _metrics_graph: dict
    _input_data: Tuple[Dataset, Optional[Dataset]]
    _current_graph_level: dict
    _legacy_metrics: Dict[str, Tuple[object, List[BaseWidgetInfo]]]

    def __init__(self):
        self._metrics = {}
        self._metric_defs = {}
        self._configuration = None
        self._metrics_graph = {}
        self._current_graph_level = self._metrics_graph
        self._legacy_metrics = {}

    def init_dataset(self, current_data: Dataset, reference_data: Optional[Dataset]):
        self._input_data = (current_data, reference_data)

    def column(self, column_name: str) -> ContextColumnData:
        return ContextColumnData(self._input_data[0].column(column_name))

    def calculate_metric(self, metric: MetricCalculationBase[TResultType]) -> TResultType:
        if metric.id not in self._current_graph_level:
            self._current_graph_level[metric.id] = {"_self": metric}
        prev_level = self._current_graph_level
        self._current_graph_level = prev_level[metric.id]
        if metric.id not in self._metrics:
            self._metrics[metric.id] = metric.call(self)
            self._metrics[metric.id]._metric = metric
        self._current_graph_level = prev_level
        return typing.cast(TResultType, self._metrics[metric.id])

    def get_metric_result(self, metric: Union[MetricId, MetricCalculationBase[TResultType]]) -> TResultType:
        if isinstance(metric, MetricId):
            return typing.cast(TResultType, self._metrics[metric])
        return self.calculate_metric(metric)

    def get_metric(self, metric: MetricId) -> MetricCalculationBase[TResultType]:
        return self._metrics_graph[metric]["_self"]

    def get_legacy_metric(self, metric: LegacyMetric[T]) -> Tuple[T, List[BaseWidgetInfo]]:
        classification = self._input_data[0]._data_definition.get_classification("default")
        input_data = InputData(
            self._input_data[1].as_dataframe() if self._input_data[1] is not None else None,
            self._input_data[0].as_dataframe(),
            ColumnMapping(
                target=classification.target if classification is not None else None,
                prediction=(classification.prediction_probas or classification.prediction_labels)
                if classification is not None
                else None,
                pos_label=classification.pos_label if isinstance(classification, BinaryClassification) else None,
                target_names=classification.labels if classification is not None else None,
            ),
            None,
            {},
            None,
            None,
        )
        dependencies = _discover_dependencies(metric)
        for _, obj in dependencies:
            (result, render) = self.get_legacy_metric(obj)
            object.__setattr__(obj, "get_result", lambda: result)
        fp = metric.get_fingerprint()
        if fp not in self._legacy_metrics:
            result = metric.calculate(input_data)
            renderer = find_metric_renderer(type(metric), DEFAULT_RENDERERS)
            object.__setattr__(metric, "get_result", lambda: result)
            self._legacy_metrics[fp] = (result, renderer.render_html(metric))
        return typing.cast(T, self._legacy_metrics[fp][0]), self._legacy_metrics[fp][1]

    @property
    def data_definition(self) -> DataDefinition:
        return self._input_data[0]._data_definition


class Snapshot:
    _report: "Report"
    _context: Context  # stores report calculation progress
    _metrics: Dict[MetricId, MetricResult]
    _widgets: List[BaseWidgetInfo]

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
        metric_results = {}
        widgets = []
        for item in self.report.items():
            if isinstance(item, (MetricPreset,)):
                for metric in item.metrics():
                    calc = metric.to_calculation()
                    metric_results[calc.id] = self.context.calculate_metric(calc)
                widgets.extend(item.calculate(metric_results).widget)
            elif isinstance(item, (MetricContainer,)):
                for metric in item.metrics(self.context):
                    calc = metric.to_calculation()
                    metric_results[calc.id] = self.context.calculate_metric(calc)
                widgets.extend(item.render(self.context, results=metric_results))
            else:
                calc = item.to_calculation()
                metric_results[calc.id] = self.context.calculate_metric(calc)
                widgets.extend(metric_results[calc.id].widget)
        self._widgets = widgets

    def _repr_html_(self):
        from evidently.renderers.html_widgets import group_widget

        results = [
            (
                metric,
                self._context.get_metric_result(metric).widget,
                self._context.get_metric_result(metric),
            )
            for metric in self.context._metrics_graph.keys()
        ]

        tests = list(chain(*[result[2].tests.values() for result in results]))
        widgets_to_render: List[BaseWidgetInfo] = [group_widget(title="", widgets=self._widgets)]

        if len(tests) > 0:
            widgets_to_render.append(metric_tests_widget(tests))

        return render_widgets(widgets_to_render)

    def dict(self) -> dict:
        return {
            "metrics": {
                metric: self.context.get_metric_result(metric).dict() for metric in self.context._metrics_graph.keys()
            },
            "tests": {
                test.id: test.dict()
                for metric in self.context._metrics_graph.keys()
                for test in self.context.get_metric_result(metric).tests
            },
        }

    def json(self) -> str:
        return json.dumps(self.dict(), cls=NumpyEncoder)


class Report:
    def __init__(
        self,
        metrics: List[Union[Metric, MetricPreset, MetricContainer]],
        metadata: Dict[str, MetadataValueType] = None,
        tags: List[str] = None,
        model_id: str = None,
        reference_id: str = None,
        batch_size: str = None,
        dataset_id: str = None,
    ):
        self._metrics = metrics
        self.metadata = metadata or {}
        self.tags = tags or []
        self._timestamp: Optional[datetime] = None
        if model_id is not None:
            self.set_model_id(model_id)
        if batch_size is not None:
            self.set_batch_size(batch_size)
        if reference_id is not None:
            self.set_reference_id(reference_id)
        if dataset_id is not None:
            self.set_dataset_id(dataset_id)

    def run(
        self,
        current_data: Dataset,
        reference_data: Optional[Dataset],
        timestamp: Optional[datetime] = None,
    ) -> Snapshot:
        self._timestamp = timestamp or datetime.now()
        snapshot = Snapshot(self)
        snapshot.run(current_data, reference_data)
        return snapshot

    def items(self) -> Sequence[Union[Metric, MetricPreset, MetricContainer]]:
        return self._metrics

    def set_batch_size(self, batch_size: str):
        self.metadata["batch_size"] = batch_size
        return self

    def set_model_id(self, model_id: str):
        self.metadata["model_id"] = model_id
        return self

    def set_reference_id(self, reference_id: str):
        self.metadata["reference_id"] = reference_id
        return self

    def set_dataset_id(self, dataset_id: str):
        self.metadata["dataset_id"] = dataset_id
        return self
