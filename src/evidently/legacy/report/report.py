import warnings
from collections import defaultdict
from datetime import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Type
from typing import Union

import pandas as pd

from evidently.legacy.base_metric import GenericInputData
from evidently.legacy.base_metric import Metric
from evidently.legacy.calculation_engine.engine import Engine
from evidently.legacy.calculation_engine.python_engine import PythonEngine
from evidently.legacy.core import IncludeOptions
from evidently.legacy.core import new_id
from evidently.legacy.metric_preset.metric_preset import MetricPreset
from evidently.legacy.metric_results import DatasetColumns
from evidently.legacy.model.dashboard import DashboardInfo
from evidently.legacy.model.widget import AdditionalGraphInfo
from evidently.legacy.model.widget import BaseWidgetInfo
from evidently.legacy.model.widget import set_source_fingerprint
from evidently.legacy.options.base import AnyOptions
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.renderers.base_renderer import DetailsInfo
from evidently.legacy.renderers.base_renderer import WidgetIdGenerator
from evidently.legacy.renderers.base_renderer import replace_widgets_ids
from evidently.legacy.suite.base_suite import MetadataValueType
from evidently.legacy.suite.base_suite import ReportBase
from evidently.legacy.suite.base_suite import Snapshot
from evidently.legacy.suite.base_suite import Suite
from evidently.legacy.suite.base_suite import find_metric_renderer
from evidently.legacy.ui.type_aliases import SnapshotID
from evidently.legacy.utils.generators import BaseGenerator

METRIC_GENERATORS = "metric_generators"
METRIC_PRESETS = "metric_presets"


class Report(ReportBase):
    _columns_info: DatasetColumns
    _first_level_metrics: List[Union[Metric]]
    _timestamp: Optional[datetime]
    metrics: List[Union[Metric, MetricPreset, BaseGenerator]]

    def __init__(
        self,
        metrics: List[Union[Metric, MetricPreset, BaseGenerator]],
        options: AnyOptions = None,
        timestamp: Optional[datetime] = None,
        id: SnapshotID = None,
        metadata: Dict[str, MetadataValueType] = None,
        tags: List[str] = None,
        model_id: str = None,
        reference_id: str = None,
        batch_size: str = None,
        dataset_id: str = None,
        name: str = None,
    ):
        super().__init__(options, name)
        # just save all metrics and metric presets
        self.metrics = metrics
        self._inner_suite = Suite(self.options)
        self._first_level_metrics = []
        if id is not None:
            warnings.warn("id argument is deprecated and has no effect", DeprecationWarning)
        self._timestamp = None
        if timestamp is not None:
            warnings.warn("timestamp argument is deprecated, use timestamp in run() method", DeprecationWarning)
            self._timestamp = timestamp
        self.metadata = metadata or {}
        self.tags = tags or []
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
        *,
        reference_data,
        current_data,
        column_mapping: Optional[ColumnMapping] = None,
        engine: Optional[Type[Engine]] = None,
        additional_data: Dict[str, Any] = None,
        timestamp: Optional[datetime] = None,
    ) -> None:
        if column_mapping is None:
            column_mapping = ColumnMapping()

        if current_data is None:
            raise ValueError("Current dataset should be present")
        self.id = new_id()
        if self._timestamp is not None:
            self.timestamp = self._timestamp
        else:
            self.timestamp = timestamp or datetime.now()
        self._first_level_metrics = []
        self._inner_suite.reset()
        self._inner_suite.set_engine(PythonEngine() if engine is None else engine())

        if self._inner_suite.context.engine is None:
            raise ValueError("No Engine is set")
        else:
            data_definition = self._inner_suite.context.get_data_definition(
                current_data,
                reference_data,
                column_mapping,
                self.options.data_definition_options.categorical_features_cardinality,
            )
        if METRIC_GENERATORS in self.metadata:
            del self.metadata[METRIC_GENERATORS]
        if METRIC_PRESETS in self.metadata:
            del self.metadata[METRIC_PRESETS]
        # get each item from metrics/presets and add to metrics list
        # do it in one loop because we want to save metrics and presets order
        for item in self.metrics:
            # if the item is a metric generator, then we need to generate metrics and add them to the report
            if isinstance(item, BaseGenerator):
                for metric in item.generate(data_definition):
                    if isinstance(metric, Metric):
                        self._first_level_metrics.append(metric)
                        self._inner_suite.add_metric(metric)

                    else:
                        # if generated item is not a metric, raise an error
                        raise ValueError(f"Incorrect metric type in generator {item}")
                if METRIC_GENERATORS not in self.metadata:
                    self.metadata[METRIC_GENERATORS] = []
                self.metadata[METRIC_GENERATORS].append(item.__class__.__name__)  # type: ignore[union-attr]
            elif isinstance(item, MetricPreset):
                metrics: List[Metric] = []

                for metric_item in item.generate_metrics(data_definition, additional_data=additional_data):
                    if isinstance(metric_item, BaseGenerator):
                        metrics.extend(metric_item.generate(data_definition))

                    else:
                        metrics.append(metric_item)

                for metric in metrics:
                    self._first_level_metrics.append(metric)
                    self._inner_suite.add_metric(metric)

                if METRIC_PRESETS not in self.metadata:
                    self.metadata[METRIC_PRESETS] = []
                self.metadata[METRIC_PRESETS].append(item.__class__.__name__)  # type: ignore[union-attr]

            elif isinstance(item, Metric):
                self._first_level_metrics.append(item)
                self._inner_suite.add_metric(item)

            else:
                raise ValueError("Incorrect item instead of a metric or metric preset was passed to Report")

        data = GenericInputData(
            reference_data, current_data, column_mapping, data_definition, additional_data=additional_data or {}
        )
        self._inner_suite.run_calculate(data)

    def as_dict(  # type: ignore[override]
        self,
        include_render: bool = False,
        include: Dict[str, IncludeOptions] = None,
        exclude: Dict[str, IncludeOptions] = None,
        **kwargs,
    ) -> dict:
        metrics = []
        include = include or {}
        exclude = exclude or {}
        for metric in self._first_level_metrics:
            renderer = find_metric_renderer(type(metric), self._inner_suite.context.renderers)
            metric_id = metric.get_id()
            metrics.append(
                {
                    "metric": metric_id,
                    "result": renderer.render_json(
                        metric,
                        include_render=include_render,
                        include=include.get(metric_id),
                        exclude=exclude.get(metric_id),
                    ),
                }
            )

        return {
            "metrics": metrics,
        }

    def as_dataframe(self, group: str = None) -> Union[Dict[str, pd.DataFrame], pd.DataFrame]:
        metrics = defaultdict(list)

        for metric in self._first_level_metrics:
            renderer = find_metric_renderer(type(metric), self._inner_suite.context.renderers)
            metric_id = metric.get_id()
            metric_fingerprint = metric.get_fingerprint()
            if group is not None and metric_id != group:
                continue
            df = renderer.render_pandas(metric)
            df["metric_id"] = metric_id
            df["metric_fingerprint"] = metric_fingerprint
            metrics[metric_id].append(df)

        result = {cls: pd.concat(val) for cls, val in metrics.items()}
        if group is None and len(result) == 1:
            return next(iter(result.values()))
        if group is None:
            return result
        if group not in result:
            raise ValueError(f"Metric group {group} not found in this report")
        return result[group]

    def _build_dashboard_info(self) -> Tuple[str, DashboardInfo, Dict[str, dict]]:
        metrics_results: List[BaseWidgetInfo] = []
        additional_graphs = []

        color_options = self.options.color_options

        id_generator = WidgetIdGenerator("")
        for metric in self._first_level_metrics:
            id_generator.base_id = metric.get_id()
            renderer = find_metric_renderer(type(metric), self._inner_suite.context.renderers)
            # set the color scheme from the report for each render
            renderer.color_options = color_options
            html_info = renderer.render_html(metric)
            set_source_fingerprint(html_info, metric)
            replace_widgets_ids(html_info, id_generator)

            for info_item in html_info:
                for additional_graph in info_item.get_additional_graphs():
                    if isinstance(additional_graph, AdditionalGraphInfo):
                        additional_graphs.append(
                            DetailsInfo(
                                title="",
                                info=additional_graph.params,
                                id=additional_graph.id,
                            )
                        )
                    else:
                        additional_graphs.append(
                            DetailsInfo(
                                title="",
                                info=additional_graph,
                                id=additional_graph.id,
                            )
                        )

            metrics_results.extend(html_info)

        return (
            "evidently_dashboard_" + str(new_id()).replace("-", ""),
            DashboardInfo(name="Report", widgets=metrics_results),
            {
                f"{item.id}": item.info.dict() if not isinstance(item.info, dict) else item.info
                for item in additional_graphs
            },
        )

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

    def _get_snapshot(self) -> Snapshot:
        snapshot = super()._get_snapshot()
        snapshot.metrics_ids = [snapshot.suite.metrics.index(m) for m in self._first_level_metrics]
        return snapshot

    @classmethod
    def _parse_snapshot(cls, snapshot: Snapshot) -> "Report":
        ctx = snapshot.suite.to_context()
        metrics = [ctx.metrics[i] for i in snapshot.metrics_ids]
        report = Report(
            metrics=metrics,
            metadata=snapshot.metadata,
            tags=snapshot.tags,
            options=snapshot.options,
            name=snapshot.name,
        )
        report.id = snapshot.id
        report.timestamp = snapshot.timestamp
        report._first_level_metrics = metrics
        report._inner_suite.context = ctx
        return report
