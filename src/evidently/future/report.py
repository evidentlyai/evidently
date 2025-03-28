import dataclasses
import json
import typing
from datetime import datetime
from itertools import chain
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import TypeVar
from typing import Union

from evidently.base_metric import InputData
from evidently.base_metric import Metric as LegacyMetric
from evidently.base_metric import MetricResult as LegacyMetricResult
from evidently.core import ColumnType
from evidently.future.container import MetricContainer
from evidently.future.container import MetricOrContainer
from evidently.future.datasets import BinaryClassification
from evidently.future.datasets import DataDefinition
from evidently.future.datasets import Dataset
from evidently.future.datasets import DatasetColumn
from evidently.future.datasets import PossibleDatasetTypes
from evidently.future.metric_types import Metric
from evidently.future.metric_types import MetricCalculationBase
from evidently.future.metric_types import MetricId
from evidently.future.metric_types import MetricResult
from evidently.future.metric_types import MetricTestResult
from evidently.future.metric_types import metric_tests_widget
from evidently.future.metric_types import render_widgets
from evidently.future.serialization import ReportModel
from evidently.future.serialization import SnapshotModel
from evidently.model.widget import BaseWidgetInfo
from evidently.model.widget import link_metric
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.renderers.base_renderer import DEFAULT_RENDERERS
from evidently.renderers.html_widgets import CounterData
from evidently.renderers.html_widgets import WidgetSize
from evidently.renderers.html_widgets import counter
from evidently.suite.base_suite import MetadataValueType
from evidently.suite.base_suite import _discover_dependencies
from evidently.suite.base_suite import find_metric_renderer
from evidently.tests.base_test import TestStatus
from evidently.utils import NumpyEncoder
from evidently.utils.data_preprocessing import create_data_definition

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


class ReferenceMetricNotFound(BaseException):
    def __init__(self, metric_id: MetricId):
        self.metric_id = metric_id

    def __str__(self):
        return f"Reference data not found for {str(self.metric_id)}"


class Context:
    _configuration: "Report"
    _metrics: Dict[MetricId, MetricResult]
    _reference_metrics: Dict[MetricId, MetricResult]
    _metrics_graph: dict
    _input_data: Tuple[Dataset, Optional[Dataset]]
    _current_graph_level: dict
    _legacy_metrics: Dict[str, Tuple[object, List[BaseWidgetInfo]]]
    _metrics_container: Dict[int, List[MetricOrContainer]]

    def __init__(self, report: "Report"):
        self._metrics = {}
        # self._metric_defs = {}
        self._configuration = report
        self._reference_metrics = {}
        self._metrics_graph = {}
        self._current_graph_level = self._metrics_graph
        self._legacy_metrics = {}
        self._metrics_container = {}

    def init_dataset(self, current_data: Dataset, reference_data: Optional[Dataset]):
        self._input_data = (current_data, reference_data)

    def column(self, column_name: str) -> ContextColumnData:
        return ContextColumnData(self._input_data[0].column(column_name))

    def calculate_metric(self, calc: MetricCalculationBase[TResultType]) -> TResultType:
        if calc.id not in self._current_graph_level:
            self._current_graph_level[calc.id] = {"_self": calc}
        prev_level = self._current_graph_level
        self._current_graph_level = prev_level[calc.id]
        if calc.id not in self._metrics:
            current_result, reference_result = calc.call(self)
            link_metric(current_result.widget, calc.to_metric())
            metric_config = calc.to_metric_config()
            current_result.set_metric_location(metric_config)
            self._metrics[calc.id] = current_result
            if reference_result is not None:
                link_metric(reference_result.widget, calc.to_metric())
                reference_result.set_metric_location(metric_config)
                self._reference_metrics[calc.id] = reference_result
            test_results = {
                tc: tc.run_test(self, calc, current_result) for tc in calc.to_metric().get_bound_tests(self)
            }
            if test_results and len(test_results) > 0:
                current_result.set_tests(list(test_results.values()))
        self._current_graph_level = prev_level
        return typing.cast(TResultType, self._metrics[calc.id])

    def get_metric_result(self, metric: Union[MetricId, Metric, MetricCalculationBase[TResultType]]) -> MetricResult:
        if isinstance(metric, MetricId):
            return self._metrics[metric]
        if isinstance(metric, Metric):
            return self._metrics[metric.metric_id]
        return self.calculate_metric(metric)

    def get_metric(self, metric: MetricId) -> MetricCalculationBase[TResultType]:
        return self._metrics_graph[metric]["_self"]

    def get_reference_metric_result(self, metric_id: MetricId) -> MetricResult:
        if metric_id not in self._reference_metrics:
            raise ReferenceMetricNotFound(metric_id)
        return self._reference_metrics[metric_id]

    def get_legacy_metric(
        self,
        metric: LegacyMetric[T],
        input_data_generator: Optional[Callable[["Context"], InputData]],
    ) -> Tuple[T, List[BaseWidgetInfo]]:
        if input_data_generator is None:
            input_data_generator = _default_input_data_generator
        input_data = input_data_generator(self)
        dependencies = _discover_dependencies(metric)
        for _, obj in dependencies:
            if isinstance(obj, LegacyMetric):
                (result, render) = self.get_legacy_metric(obj, input_data_generator)
                object.__setattr__(obj, "get_result", lambda: result)
            else:
                raise ValueError(f"unexpected type {type(obj)}")
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

    @property
    def configuration(self) -> "Report":
        return self._configuration

    @property
    def has_reference(self) -> bool:
        return self._input_data[1] is not None

    def metrics_container(self, metric_container_hash: int) -> Optional[List[MetricOrContainer]]:
        return self._metrics_container.get(metric_container_hash)

    def set_metric_container_data(self, metric_container_hash: int, items: List[MetricOrContainer]) -> None:
        self._metrics_container[metric_container_hash] = items


def _default_input_data_generator(context: "Context") -> InputData:
    classification = context.data_definition.get_classification("default")
    ranking = context.data_definition.get_ranking("default")
    reference = context._input_data[1].as_dataframe() if context._input_data[1] is not None else None
    current = context._input_data[0].as_dataframe()
    prediction: Optional[Union[str, List[str]]]
    user_id: Optional[str] = None
    target: Optional[str] = None
    if classification is not None:
        if isinstance(classification.prediction_probas, list):
            prediction = classification.prediction_probas
        elif classification.prediction_probas not in current.columns:
            prediction = classification.prediction_labels
        else:
            prediction = classification.prediction_probas
        target = classification.target
    else:
        prediction = None
    if ranking is not None:
        user_id = ranking.user_id
        prediction = ranking.prediction
        target = ranking.target
    mapping = ColumnMapping(
        id=context.data_definition.id_column,
        datetime=context.data_definition.timestamp,
        target=target,
        prediction=prediction,
        pos_label=classification.pos_label if isinstance(classification, BinaryClassification) else None,
        target_names=classification.labels if classification is not None else None,
        user_id=user_id,
        numerical_features=[x for x in context.data_definition.get_columns([ColumnType.Numerical])],
        categorical_features=[x for x in context.data_definition.get_columns([ColumnType.Categorical])],
        text_features=[x for x in context.data_definition.get_columns([ColumnType.Text])],
        datetime_features=[x for x in context.data_definition.get_columns([ColumnType.Datetime])],
    )
    definition = create_data_definition(
        reference,
        current,
        mapping,
    )
    input_data = InputData(
        reference,
        current,
        mapping,
        definition,
        {},
        None,
        None,
    )
    return input_data


def metric_tests_stats(tests: List[MetricTestResult]) -> BaseWidgetInfo:
    statuses = [TestStatus.SUCCESS, TestStatus.WARNING, TestStatus.FAIL, TestStatus.ERROR]
    status_stats: Dict[TestStatus, int] = {}
    for test in tests:
        status_stats[test.status] = status_stats.get(test.status, 0) + 1
    stats = counter(
        title="",
        size=WidgetSize.FULL,
        counters=[CounterData(status.value, str(status_stats.get(status, 0))) for status in statuses],
    )
    stats.params["v2_test"] = True
    return stats


@dataclasses.dataclass
class SnapshotItem:
    metric_id: Optional[MetricId]
    widgets: List[BaseWidgetInfo]


class Snapshot:
    _report: "Report"
    _context: Context  # stores report calculation progress
    _metrics: Dict[MetricId, MetricResult]
    _snapshot_item: List[SnapshotItem]
    _widgets: List[BaseWidgetInfo]
    _tests_widgets: List[BaseWidgetInfo]
    _top_level_metrics: List[MetricId]
    _timestamp: datetime
    _tags: List[str]
    _metadata: Dict[str, MetadataValueType]

    def __init__(
        self,
        report: "Report",
        timestamp: datetime,
        metadata: Dict[str, MetadataValueType],
        tags: List[str],
    ):
        self._report = report
        self._context = Context(report)
        self._snapshot_item = []
        self._metrics = {}
        self._top_level_metrics = []
        self._tests_widgets = []
        self._timestamp = timestamp
        self._tags = tags
        self._metadata = metadata

    @property
    def context(self) -> Context:
        return self._context

    @property
    def report(self) -> "Report":
        return self._report

    def _run_items(
        self,
        items: Sequence[MetricOrContainer],
        metric_results: Dict[MetricId, MetricResult],
    ) -> Tuple[List[SnapshotItem], List[BaseWidgetInfo]]:
        widgets: List[BaseWidgetInfo] = []
        snapshot_items: List[SnapshotItem] = []
        for item in items:
            if isinstance(item, MetricContainer):
                container_items, container_widgets = self._run_items(item.metrics(self.context), metric_results)
                widget = item.render(self.context, [(v.metric_id, v.widgets) for v in container_items])
                widgets.extend(widget)
                snapshot_items.append(SnapshotItem(None, widget))
            else:
                calc = item.to_calculation()
                metric_results[calc.id] = self.context.calculate_metric(calc)
                widget = metric_results[calc.id].get_widgets()
                widgets.extend(widget)
                snapshot_items.append(SnapshotItem(calc.id, widget))
        return snapshot_items, widgets

    def run(self, current_data: Dataset, reference_data: Optional[Dataset]):
        self.context.init_dataset(current_data, reference_data)
        self._metrics = {}
        self._snapshot_item, self._widgets = self._run_items(self.report.items(), self._metrics)
        self._top_level_metrics = list(self.context._metrics_graph.keys())
        metrics_results = [self._metrics.get(result) for result in self._top_level_metrics]
        tests = list(chain(*[result.tests for result in metrics_results if result is not None]))
        if len(tests) > 0:
            self._tests_widgets = [
                metric_tests_stats(tests),
                metric_tests_widget(tests),
            ]

    def _repr_html_(self):
        from evidently.renderers.html_widgets import group_widget

        widgets_to_render: List[BaseWidgetInfo] = [group_widget(title="", widgets=self._widgets)] + self._tests_widgets

        return render_widgets(widgets_to_render)

    def render_only_fingerprint(self, fingerprint: str):
        from IPython.display import HTML

        from evidently.renderers.html_widgets import group_widget

        results = [
            (
                metric,
                self._metrics[metric].get_widgets(),
                self._metrics[metric],
            )
            for metric in self._top_level_metrics
        ]

        tests = list(chain(*[result[2].tests for result in results]))
        widgets = [w for w in self._widgets if fingerprint in (w.linked_metrics or [])]
        widgets_to_render: List[BaseWidgetInfo] = [group_widget(title="", widgets=widgets)]

        if len(tests) > 0:
            widgets_to_render.append(metric_tests_stats(tests))
            widgets_to_render.append(metric_tests_widget(tests))
        return HTML(render_widgets(widgets_to_render))

    def json(self) -> str:
        return json.dumps(self.dict(), cls=NumpyEncoder)

    def save_html(self, filename: Union[str, typing.IO]):
        if isinstance(filename, str):
            with open(filename, "w", encoding="utf-8") as out_file:
                out_file.write(self._repr_html_())

    def save_json(self, filename: Union[str, typing.IO]):
        if isinstance(filename, str):
            with open(filename, "w", encoding="utf-8") as out_file:
                json.dump(self.dict(), out_file, cls=NumpyEncoder)

    def _to_v1(self):
        from evidently.future.backport import snapshot_v2_to_v1

        return snapshot_v2_to_v1(self)

    def dumps(self) -> str:
        return json.dumps(self.dump_dict(), cls=NumpyEncoder)

    def dump_dict(self) -> dict:
        snapshot = SnapshotModel(
            report=ReportModel(items=[]),
            timestamp=self._timestamp,
            metadata=self._metadata,
            tags=self._tags,
            metric_results=self._metrics,
            top_level_metrics=self._top_level_metrics,
            widgets=self._widgets,
            tests_widgets=self._tests_widgets,
        )
        return snapshot.dict()

    @staticmethod
    def loads(data: str) -> "Snapshot":
        return Snapshot.load_dict(json.loads(data))

    @staticmethod
    def load_dict(data: dict) -> "Snapshot":
        model = SnapshotModel.parse_obj(data)
        snapshot = Snapshot(report=Report([]), timestamp=model.timestamp, metadata=model.metadata, tags=model.tags)
        snapshot._metrics = model.metric_results
        snapshot._top_level_metrics = model.top_level_metrics
        snapshot._widgets = model.widgets
        snapshot._tests_widgets = model.tests_widgets
        return snapshot

    def dict(self) -> dict:
        return {
            "metrics": [
                self._metrics[metric].to_dict() if self._metrics.get(metric) is not None else {}
                for metric in self._top_level_metrics
            ],
            "tests": [
                test_result.dict() for metric in self._top_level_metrics for test_result in self._metrics[metric].tests
            ],
        }


class Report:
    metrics: List[MetricOrContainer]
    metadata: Dict[str, MetadataValueType]
    tags: List[str]
    include_tests: bool

    def __init__(
        self,
        metrics: List[MetricOrContainer],
        metadata: Dict[str, MetadataValueType] = None,
        tags: List[str] = None,
        model_id: str = None,
        reference_id: str = None,
        batch_size: str = None,
        dataset_id: str = None,
        include_tests: bool = False,
    ):
        self.metrics = metrics
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
        self.include_tests = include_tests

    def run(
        self,
        current_data: PossibleDatasetTypes,
        reference_data: Optional[PossibleDatasetTypes] = None,
        timestamp: Optional[datetime] = None,
        metadata: Dict[str, MetadataValueType] = None,
        tags: List[str] = None,
    ) -> Snapshot:
        current_dataset = Dataset.from_any(current_data)
        reference_dataset = Dataset.from_any(reference_data) if reference_data is not None else None
        _timestamp = timestamp or datetime.now()
        _metadata = self.metadata.copy()
        if metadata is not None:
            _metadata.update(metadata)
        _tags = self.tags.copy()
        if tags is not None:
            _tags.extend(tags)
        snapshot = Snapshot(self, _timestamp, _metadata, _tags)
        snapshot.run(current_dataset, reference_dataset)
        return snapshot

    def items(self) -> Sequence[MetricOrContainer]:
        return self.metrics

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
