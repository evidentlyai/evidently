import dataclasses
import json
import pathlib
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

from typing_extensions import TypeAlias

from evidently.core.base_types import Label
from evidently.core.metric_types import Metric
from evidently.core.metric_types import MetricCalculationBase
from evidently.core.metric_types import MetricId
from evidently.core.metric_types import MetricResult
from evidently.core.metric_types import MetricTestResult
from evidently.core.metric_types import metric_tests_widget
from evidently.core.metric_types import render_widgets
from evidently.core.serialization import ReportModel
from evidently.core.serialization import SnapshotModel
from evidently.legacy.base_metric import InputData
from evidently.legacy.base_metric import Metric as LegacyMetric
from evidently.legacy.base_metric import MetricResult as LegacyMetricResult
from evidently.legacy.core import ColumnType
from evidently.legacy.model.widget import BaseWidgetInfo
from evidently.legacy.model.widget import link_metric
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.renderers.base_renderer import DEFAULT_RENDERERS
from evidently.legacy.renderers.html_widgets import CounterData
from evidently.legacy.renderers.html_widgets import WidgetSize
from evidently.legacy.renderers.html_widgets import counter
from evidently.legacy.suite.base_suite import MetadataValueType
from evidently.legacy.suite.base_suite import _discover_dependencies
from evidently.legacy.suite.base_suite import find_metric_renderer
from evidently.legacy.tests.base_test import TestStatus
from evidently.legacy.utils import NumpyEncoder
from evidently.legacy.utils.data_preprocessing import create_data_definition
from evidently.pydantic_utils import Fingerprint

from .container import MetricContainer
from .container import MetricOrContainer
from .datasets import BinaryClassification
from .datasets import DataDefinition
from .datasets import Dataset
from .datasets import DatasetColumn
from .datasets import PossibleDatasetTypes

TResultType = TypeVar("TResultType", bound=MetricResult)
T = TypeVar("T", bound=LegacyMetricResult)


class ContextColumnData:
    """Wrapper for column data in a `Context` for metric calculations.

    Provides access to column information and categorical labels during metric computation.
    Used internally by metrics to access column data and type information.
    """

    _column: DatasetColumn
    _labels: Optional[List[object]]

    def __init__(self, column: DatasetColumn):
        """Initialize with a dataset column.

        Args:
        * `column`: The `DatasetColumn` to wrap.
        """
        self._column = column
        self._labels = None

    def labels(self):
        """Get unique labels for a categorical column.

        Returns:
        * List of unique label values in the column.

        Raises:
        * `AttributeError`: If the column is not categorical.
        """
        if self.column_type != ColumnType.Categorical:
            raise AttributeError("labels() is not supported for non-categorical columns")
        if self._labels is None:
            self._labels = list(self._column.data.unique())
        return self._labels

    @property
    def column_type(self) -> ColumnType:
        """Get the type of the column.

        Returns:
        * `ColumnType`: The type of the column (e.g., Numerical, Categorical, Text).
        """
        return self._column.type


class ReferenceMetricNotFound(BaseException):
    """Exception raised when reference metric result is requested but not available.

    This exception is raised when trying to access a reference metric result
    that was not computed (e.g., when no reference dataset was provided).
    """

    def __init__(self, metric_id: MetricId):
        """Initialize the exception.

        Args:
        * `metric_id`: The ID of the metric that was not found.
        """
        self.metric_id = metric_id

    def __str__(self):
        return f"Reference data not found for {str(self.metric_id)}"


class Context:
    """Execution context for metric calculations during report runs.

    The `Context` manages the state and data during metric computation. It provides:
    - Access to current and reference datasets
    - Caching of computed metric results
    - Access to column data and data definitions
    - Support for metric dependencies and containers

    The `Context` is created automatically when you call `Report.run()` and is passed
    to metrics during calculation. You typically don't create `Context` objects directly.
    """

    _configuration: "Report"
    _metrics: Dict[MetricId, MetricResult]
    _reference_metrics: Dict[MetricId, MetricResult]
    _metrics_graph: dict
    _input_data: Tuple[Dataset, Optional[Dataset]]
    _additional_data: Dict[str, Dataset]
    _current_graph_level: dict
    _legacy_metrics: Dict[str, Tuple[object, List[BaseWidgetInfo]]]
    _metrics_container: Dict[Fingerprint, List[MetricOrContainer]]
    _labels: Optional[List[Label]]

    def __init__(self, report: "Report"):
        """Initialize the context with a report configuration.

        Args:
        * `report`: The `Report` configuration.
        """
        self._metrics = {}
        # self._metric_defs = {}
        self._configuration = report
        self._reference_metrics = {}
        self._metrics_graph = {}
        self._current_graph_level = self._metrics_graph
        self._legacy_metrics = {}
        self._metrics_container = {}
        self._labels = None
        self._additional_data = {}

    def init_dataset(
        self,
        current_data: Dataset,
        reference_data: Optional[Dataset],
        additional_data: Optional[Dict[str, Dataset]] = None,
    ):
        """Initialize the context with datasets for metric computation.

        Args:
        * `current_data`: The current dataset to evaluate.
        * `reference_data`: Optional reference dataset for comparison.
        * `additional_data`: Optional dictionary of additional datasets by name.
        """
        self._input_data = (current_data, reference_data)
        self._additional_data = additional_data or {}

    def column(self, column_name: str) -> ContextColumnData:
        """Get column data wrapper for a specific column.

        Args:
        * `column_name`: Name of the column to access.

        Returns:
        * `ContextColumnData`: Wrapper object providing column data and type information.
        """
        return ContextColumnData(self._input_data[0].column(column_name))

    def calculate_metric(self, calc: MetricCalculationBase[TResultType]) -> TResultType:
        """Calculate a metric and cache the result.

        Computes the metric if not already cached, handles dependencies,
        runs associated tests, and returns the result.

        Args:
        * `calc`: The metric calculation to execute.

        Returns:
        * `TResultType`: The computed metric result.
        """
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
        """Get the result of a metric computation.

        Returns cached result if available, otherwise calculates the metric.

        Args:
        * `metric`: The metric identifier, metric object, or calculation to get results for.

        Returns:
        * `MetricResult`: The computed metric result.
        """
        if isinstance(metric, MetricId):
            return self._metrics[metric]
        if isinstance(metric, Metric):
            return self._metrics[metric.metric_id]
        return self.calculate_metric(metric)

    def get_metric(self, metric: MetricId) -> MetricCalculationBase[TResultType]:
        """Get the metric calculation object for a metric ID.

        Args:
        * `metric`: The metric ID to look up.

        Returns:
        * `MetricCalculationBase`: The metric calculation object.
        """
        return self._metrics_graph[metric]["_self"]

    def get_reference_metric_result(self, metric_id: MetricId) -> MetricResult:
        """Get the reference metric result for a metric.

        Args:
        * `metric_id`: The metric ID to get reference results for.

        Returns:
        * `MetricResult`: The reference metric result.

        Raises:
        * `ReferenceMetricNotFound`: If reference data was not provided or metric was not computed.
        """
        if metric_id not in self._reference_metrics:
            raise ReferenceMetricNotFound(metric_id)
        return self._reference_metrics[metric_id]

    def get_legacy_metric(
        self,
        metric: LegacyMetric[T],
        input_data_generator: Optional[Callable[["Context", Optional[str]], InputData]],
        task_name: Optional[str],
    ) -> Tuple[T, List[BaseWidgetInfo]]:
        """Calculate a legacy metric and return result with widgets.

        Supports legacy (v1) metrics for backward compatibility. Handles dependencies
        and caches results.

        Args:
        * `metric`: The legacy metric to calculate.
        * `input_data_generator`: Optional function to generate input data. Uses default if None.
        * `task_name`: Optional task name for classification/ranking metrics.

        Returns:
        * Tuple of (metric result, list of HTML widgets).
        """
        if input_data_generator is None:
            input_data_generator = _default_input_data_generator
        input_data = input_data_generator(self, task_name)
        dependencies = _discover_dependencies(metric)
        for _, obj in dependencies:
            if isinstance(obj, LegacyMetric):
                (result, render) = self.get_legacy_metric(obj, input_data_generator, task_name)
                object.__setattr__(obj, "get_result", lambda: result)
            else:
                raise ValueError(f"unexpected type {type(obj)}")
        fp = metric.get_fingerprint() + ":task:" + (task_name or "")
        if fp not in self._legacy_metrics:
            result = metric.calculate(input_data)
            renderer = find_metric_renderer(type(metric), DEFAULT_RENDERERS)
            object.__setattr__(metric, "get_result", lambda: result)
            self._legacy_metrics[fp] = (result, renderer.render_html(metric))
        return typing.cast(T, self._legacy_metrics[fp][0]), self._legacy_metrics[fp][1]

    @property
    def data_definition(self) -> DataDefinition:
        """Get the data definition for the current dataset.

        Returns:
        * `DataDefinition`: The column mapping and type information.
        """
        return self._input_data[0]._data_definition

    @property
    def configuration(self) -> "Report":
        """Get the report configuration.

        Returns:
        * `Report`: The report that created this context.
        """
        return self._configuration

    @property
    def has_reference(self) -> bool:
        """Check if reference data is available.

        Returns:
        * `bool`: True if reference dataset was provided, False otherwise.
        """
        return self._input_data[1] is not None

    @property
    def additional_data(self) -> Dict[str, Dataset]:
        """Get additional datasets by name.

        Returns:
        * Dictionary mapping dataset names to `Dataset` objects.
        """
        return self._additional_data or {}

    def metrics_container(self, metric_container_fingerprint: Fingerprint) -> Optional[List[MetricOrContainer]]:
        """Get metrics for a container by fingerprint.

        Args:
        * `metric_container_fingerprint`: The fingerprint of the container.

        Returns:
        * Optional list of metrics/containers, or None if not found.
        """
        return self._metrics_container.get(metric_container_fingerprint)

    def set_metric_container_data(
        self, metric_container_fingerprint: Fingerprint, items: List[MetricOrContainer]
    ) -> None:
        """Store metrics for a container.

        Args:
        * `metric_container_fingerprint`: The fingerprint of the container.
        * `items`: List of metrics or containers to store.
        """
        self._metrics_container[metric_container_fingerprint] = items

    def get_labels(self, target: str, prediction: Optional[str]) -> List[Label]:
        """Get all unique labels from target and prediction columns.

        Collects labels from both current and reference datasets if available.

        Args:
        * `target`: Name of the target column.
        * `prediction`: Optional name of the prediction column.

        Returns:
        * List of unique label values across both datasets.
        """
        if self._labels is not None:
            return self._labels
        current_labels = (
            set(self._input_data[0].column(target).data)  # type: ignore[call-overload]
            | set([] if prediction is None else self._input_data[0].column(prediction).data)  # type: ignore[call-overload]
        )
        ref_data = self._input_data[1]
        reference_labels = (
            set()
            if not self.has_reference or ref_data is None
            else (
                set(ref_data.column(target).data)  # type: ignore[call-overload]
                | set([] if prediction is None else ref_data.column(prediction).data)  # type: ignore[call-overload]
            )
        )
        self._labels = list(current_labels | reference_labels)
        return self._labels


def _default_input_data_generator(context: "Context", task_name: Optional[str]) -> InputData:
    if task_name is None:
        classification = None
        ranking = None
    else:
        classification = context.data_definition.get_classification(task_name)
        ranking = context.data_definition.get_ranking(task_name)
    reference = context._input_data[1].as_dataframe() if context._input_data[1] is not None else None
    current = context._input_data[0].as_dataframe()
    prediction: Optional[Union[str, List[str]]]
    user_id: Optional[str] = None
    item_id: Optional[str] = None
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
        item_id = ranking.item_id
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
        item_id=item_id,
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

    additional_dataframes = {}
    for key, dataset in context._additional_data.items():
        additional_dataframes[key] = dataset.as_dataframe()

    input_data = InputData(
        reference,
        current,
        mapping,
        definition,
        additional_dataframes,
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
    """Represents a single metric result item in a snapshot.

    Contains the metric identifier and associated visualization widgets.
    Used internally to organize metric results in a `Snapshot`.
    """

    metric_id: Optional[MetricId]
    """Optional identifier of the metric."""
    widgets: List[BaseWidgetInfo]
    """List of HTML widgets for visualizing the metric results."""


class Snapshot:
    """Snapshot contains the computed results of running a `Report` on datasets.

    A `Snapshot` (also aliased as `Run`) contains:
    - Computed metric results for each metric in the report
    - Test results if tests were configured
    - Metadata, tags, and timestamp
    - Methods to export results as HTML, JSON, or Python dictionary

    You typically create a `Snapshot` by calling `report.run()` with your datasets.

    Example:
    ```python
    report = Report([DataSummaryPreset()])
    snapshot = report.run(current_data, reference_data)
    snapshot.save_html("report.html")  # Export as HTML
    snapshot.json()  # Export as JSON string
    snapshot.dict()  # Export as Python dictionary
    ```
    """

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
    _name: Optional[str]

    def __init__(
        self,
        report: "Report",
        name: Optional[str],
        timestamp: datetime,
        metadata: Dict[str, MetadataValueType],
        tags: List[str],
    ):
        """Initialize a `Snapshot` (typically created by `Report.run()`, not called directly)."""
        self._name = name
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

    def run(
        self,
        current_data: Dataset,
        reference_data: Optional[Dataset],
        additional_data: Optional[Dict[str, Dataset]] = None,
    ):
        """Run the report computation on datasets (typically called by `Report.run()`, not directly)."""
        self.context.init_dataset(current_data, reference_data, additional_data)
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

    def get_html_str(self, as_iframe: bool):
        """Get HTML representation of the snapshot.

        Args:
        * `as_iframe`: If True, returns HTML suitable for embedding in iframe. If False, returns standalone HTML.

        Returns:
        * HTML string representation of the report
        """
        from evidently.legacy.renderers.html_widgets import group_widget

        widgets_to_render: List[BaseWidgetInfo] = [group_widget(title="", widgets=self._widgets)] + self._tests_widgets

        return render_widgets(widgets_to_render, as_iframe=as_iframe)

    def _repr_html_(self):
        return self.get_html_str(as_iframe=True)

    def render_only_fingerprint(self, fingerprint: str):
        """Render HTML for a specific metric by fingerprint in Jupyter notebook.

        Displays only the metric matching the given fingerprint, useful for
        selectively showing specific metrics in notebooks.

        Args:
        * `fingerprint`: The fingerprint identifier of the metric to render.

        Returns:
        * IPython HTML display object for the metric widgets.
        """
        from IPython.display import HTML

        from evidently.legacy.renderers.html_widgets import group_widget

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
        """Export snapshot results as JSON string.

        Returns:
        * JSON string containing metrics and test results
        """
        return json.dumps(self.dict(), cls=NumpyEncoder)

    def save_html(self, filename: Union[str, typing.IO]):
        """Save snapshot as HTML file.

        Args:
        * `filename`: File path (string) or file-like object to write HTML to
        """
        if isinstance(filename, str):
            with open(filename, "w", encoding="utf-8") as out_file:
                out_file.write(self.get_html_str(as_iframe=False))

    def save_json(self, filename: Union[str, typing.IO]):
        """Save snapshot as JSON file.

        Args:
        * `filename`: File path (string) or file-like object to write JSON to
        """
        if isinstance(filename, str):
            with open(filename, "w", encoding="utf-8") as out_file:
                json.dump(self.dict(), out_file, cls=NumpyEncoder)

    def _to_v1(self):
        from evidently.ui.backport import snapshot_v2_to_v1

        return snapshot_v2_to_v1(self)

    def dumps(self) -> str:
        """Export snapshot as JSON string (full serialization format).

        Returns:
        * JSON string with complete snapshot data including widgets and metadata
        """
        return json.dumps(self.dump_dict(), cls=NumpyEncoder)

    def dump_dict(self) -> dict:
        """Export snapshot as Python dictionary (full serialization format).

        Returns:
        * Dictionary with complete snapshot data including widgets and metadata
        """
        return self.to_snapshot_model().dict()

    def to_snapshot_model(self):
        """Convert snapshot to serialization model.

        Returns:
        * `SnapshotModel` object for serialization
        """
        snapshot = SnapshotModel(
            report=ReportModel(items=[]),
            name=self._name,
            timestamp=self._timestamp,
            metadata=self._metadata,
            tags=self._tags,
            metric_results=self._metrics,
            top_level_metrics=self._top_level_metrics,
            widgets=self._widgets,
            tests_widgets=self._tests_widgets,
        )
        return snapshot

    @staticmethod
    def load(path: Union[str, pathlib.Path]):
        """Load a snapshot from a JSON file.

        Args:
        * `path`: Path to JSON file containing snapshot data

        Returns:
        * `Snapshot` object loaded from file
        """
        with open(path, "r", encoding="utf-8") as in_file:
            return Snapshot.loads(in_file.read())

    @staticmethod
    def loads(data: str) -> "Snapshot":
        """Load a snapshot from a JSON string.

        Args:
        * `data`: JSON string containing snapshot data

        Returns:
        * `Snapshot` object loaded from string
        """
        return Snapshot.load_dict(json.loads(data))

    @staticmethod
    def load_dict(data: dict) -> "Snapshot":
        """Load a snapshot from a Python dictionary.

        Args:
        * `data`: Dictionary containing snapshot data

        Returns:
        * `Snapshot` object loaded from dictionary
        """
        model = SnapshotModel.parse_obj(data)
        return Snapshot.load_model(model)

    @staticmethod
    def load_model(model: SnapshotModel) -> "Snapshot":
        """Load a snapshot from a `SnapshotModel` object.

        Args:
        * `model`: `SnapshotModel` object

        Returns:
        * `Snapshot` object loaded from model
        """
        snapshot = Snapshot(
            report=Report([]),
            name=model.name,
            timestamp=model.timestamp,
            metadata=model.metadata,
            tags=model.tags,
        )
        snapshot._metrics = model.metric_results
        snapshot._top_level_metrics = model.top_level_metrics
        snapshot._widgets = model.widgets
        snapshot._tests_widgets = model.tests_widgets
        return snapshot

    def dict(self) -> dict:
        """Export snapshot results as Python dictionary (metrics and tests only).

        Returns:
        * Dictionary with metrics and test results (simplified format)
        """
        return {
            "metrics": [
                self._metrics[metric].to_dict() if self._metrics.get(metric) is not None else {}
                for metric in self._top_level_metrics
            ],
            "tests": [test_result.dict() for test_result in self.tests_results],
        }

    @property
    def tests_results(self):
        """Get all test results from all metrics in the snapshot.

        Returns:
        * List of all test results across all metrics
        """
        return [test_result for metric in self._top_level_metrics for test_result in self._metrics[metric].tests]

    @property
    def metric_results(self):
        """Get all metric results from the snapshot.

        Returns:
        * Dictionary mapping metric IDs to their results
        """
        return self._metrics

    def get_name(self) -> Optional[str]:
        """Get the name of this snapshot.

        Returns:
        * `Snapshot` name or None if not set
        """
        return self._name

    def set_name(self, name: str):
        """Set the name of this snapshot.

        Args:
        * `name`: Name to assign to the snapshot
        """
        self._name = name


Run: TypeAlias = Snapshot


class Report:
    """Report lets you structure and run evaluations on the dataset or column-level.

    You can generate `Report` objects after you get descriptors, or for any existing dataset like a table with ML model logs.
    Use `Report` to:
    - Summarize computed text descriptors across all inputs
    - Analyze any tabular dataset (descriptive stats, quality, drift)
    - Evaluate AI system performance (regression, classification, ranking, etc.)

    Each `Report` runs a computation and visualizes a set of Metrics and conditional Tests.
    If you pass two datasets, you get a side-by-side comparison.

    Use `Dataset` to prepare your data and `DataDefinition` to map columns. The `run()` method
    returns a `Snapshot` object with computed results.

    **Documentation**: See [Report Guide](https://docs.evidentlyai.com/docs/library/report) for detailed usage.

    Using a preset:
    ```python
    from evidently import Report, Dataset
    from evidently.presets import DataSummaryPreset

    report = Report([DataSummaryPreset()])
    dataset = Dataset.from_pandas(df, data_definition=DataDefinition())
    snapshot = report.run(dataset, None)
    ```

    Using custom metrics:
    ```python
    from evidently.metrics import ColumnCount, ValueStats

    report = Report([ColumnCount(), ValueStats(column="target")])
    snapshot = report.run(dataset, None)
    ```

    With reference data for drift detection:
    ```python
    from evidently.presets import DataDriftPreset

    report = Report([DataDriftPreset()])
    snapshot = report.run(current_dataset, reference_dataset)
    ```
    """

    metrics: List[MetricOrContainer]
    """List of metrics or metric containers to include in the report."""
    metadata: Dict[str, MetadataValueType]
    """Dictionary of metadata key-value pairs."""
    tags: List[str]
    """List of tags for categorizing reports."""
    include_tests: bool
    """Whether to include automatic tests for metrics."""

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
        """Initialize a Report with metrics and optional metadata.

        The constructor maps parameters to class attributes. Additional convenience parameters
        (`model_id`, `reference_id`, `batch_size`, `dataset_id`) are stored in the `metadata` dictionary.
        """
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
        additional_data: Optional[Dict[str, PossibleDatasetTypes]] = None,
        timestamp: Optional[datetime] = None,
        metadata: Dict[str, MetadataValueType] = None,
        tags: List[str] = None,
        name: Optional[str] = None,
    ) -> Snapshot:
        """Run the report on datasets and return a `Snapshot` with computed results.

        Args:
        * `current_data`: Current dataset to evaluate (`pandas.DataFrame` or `Dataset`)
        * `reference_data`: Optional reference dataset for comparison/drift detection (`pandas.DataFrame` or `Dataset`)
        * `additional_data`: Optional dictionary of additional datasets by name
        * `timestamp`: Optional timestamp for the snapshot (defaults to now)
        * `metadata`: Optional metadata to merge with report metadata
        * `tags`: Optional tags to merge with report tags
        * `name`: Optional name for the snapshot

        Returns:
        * `Snapshot`: Object containing computed metric results, tests, and visualizations.
          Use `Snapshot.save_html()`, `Snapshot.json()`, or `Snapshot.dict()` to export results.

        Example:
        ```python
        from evidently import Report, Dataset
        from evidently.presets import DataSummaryPreset

        report = Report([DataSummaryPreset()])
        dataset = Dataset.from_pandas(df, data_definition=DataDefinition())
        snapshot = report.run(dataset, None, name="daily_check")
        snapshot.save_html("report.html")
        ```
        """
        current_dataset = Dataset.from_any(current_data)
        reference_dataset = Dataset.from_any(reference_data) if reference_data is not None else None

        additional_datasets = None
        if additional_data is not None:
            additional_datasets = {}
            for key, data in additional_data.items():
                additional_datasets[key] = Dataset.from_any(data)

        _timestamp = timestamp or datetime.now()
        _metadata = self.metadata.copy()
        if metadata is not None:
            _metadata.update(metadata)
        _tags = self.tags.copy()
        if tags is not None:
            _tags.extend(tags)
        snapshot = Snapshot(self, name, _timestamp, _metadata, _tags)
        snapshot.run(current_dataset, reference_dataset, additional_datasets)
        return snapshot

    def items(self) -> Sequence[MetricOrContainer]:
        """Get the list of metrics and containers in this report.

        Returns:
        * Sequence of metrics and metric containers configured in the report
        """
        return self.metrics

    def set_batch_size(self, batch_size: str):
        """Set the batch size identifier in report metadata.

        Args:
        * `batch_size`: Batch size identifier string

        Returns:
        * Self for method chaining
        """
        self.metadata["batch_size"] = batch_size
        return self

    def set_model_id(self, model_id: str):
        """Set the model identifier in report metadata.

        Args:
        * `model_id`: Model identifier string

        Returns:
        * Self for method chaining
        """
        self.metadata["model_id"] = model_id
        return self

    def set_reference_id(self, reference_id: str):
        """Set the reference dataset identifier in report metadata.

        Args:
        * `reference_id`: Reference dataset identifier string

        Returns:
        * Self for method chaining
        """
        self.metadata["reference_id"] = reference_id
        return self

    def set_dataset_id(self, dataset_id: str):
        """Set the dataset identifier in report metadata.

        Args:
        * `dataset_id`: Dataset identifier string

        Returns:
        * Self for method chaining
        """
        self.metadata["dataset_id"] = dataset_id
        return self
