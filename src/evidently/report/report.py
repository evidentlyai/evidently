import uuid
from datetime import datetime
from typing import List
from typing import Optional
from typing import Union

import dataclasses
import pandas as pd

from evidently import ColumnMapping
from evidently.metric_preset.metric_preset import MetricPreset
from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.model.dashboard import DashboardInfo
from evidently.model.widget import AdditionalGraphInfo
from evidently.renderers.base_renderer import DetailsInfo
from evidently.suite.base_suite import Display
from evidently.suite.base_suite import Suite
from evidently.suite.base_suite import find_metric_renderer
from evidently.utils.data_operations import DatasetColumns
from evidently.utils.data_operations import process_columns
from evidently.utils.generators import BaseGenerator


class Report(Display):
    _inner_suite: Suite
    _columns_info: DatasetColumns
    _first_level_metrics: List[Union[Metric]]
    metrics: List[Union[Metric, MetricPreset, BaseGenerator]]

    def __init__(self, metrics: List[Union[Metric, MetricPreset, BaseGenerator]]):
        super().__init__()
        # just save all metrics and metric presets
        self.metrics = metrics
        self._inner_suite = Suite()
        self._first_level_metrics = []

    def run(
        self,
        *,
        reference_data: Optional[pd.DataFrame],
        current_data: pd.DataFrame,
        column_mapping: Optional[ColumnMapping] = None,
    ) -> None:
        if column_mapping is None:
            column_mapping = ColumnMapping()

        if current_data is None:
            raise ValueError("Current dataset should be present")

        self._columns_info = process_columns(current_data, column_mapping)
        data = InputData(reference_data, current_data, column_mapping)

        # get each item from metrics/presets and add to metrics list
        # do it in one loop because we want to save metrics and presets order
        for item in self.metrics:
            # if the item is a metric generator, then we need to generate metrics and add them to the report
            if isinstance(item, BaseGenerator):
                for metric in item.generate(columns_info=self._columns_info):
                    if isinstance(metric, Metric):
                        self._first_level_metrics.append(metric)
                        self._inner_suite.add_metric(metric)

                    else:
                        # if generated item is not a metric, raise an error
                        raise ValueError(f"Incorrect metric type in generator {item}")

            elif isinstance(item, MetricPreset):
                metrics = []

                for metric_item in item.generate_metrics(data=data, columns=self._columns_info):
                    if isinstance(metric_item, BaseGenerator):
                        metrics.extend(metric_item.generate(columns_info=self._columns_info))

                    else:
                        metrics.append(metric_item)

                for metric in metrics:
                    self._first_level_metrics.append(metric)
                    self._inner_suite.add_metric(metric)

            elif isinstance(item, Metric):
                self._first_level_metrics.append(item)
                self._inner_suite.add_metric(item)

            else:
                raise ValueError("Incorrect item instead of a metric or metric preset was passed to Report")

        self._inner_suite.verify()
        self._inner_suite.run_calculate(data)

    def as_dict(self) -> dict:
        metrics_dicts = {}
        for metric in self._first_level_metrics:
            renderer = find_metric_renderer(type(metric), self._inner_suite.context.renderers)
            metrics_dicts[metric.get_id()] = renderer.render_json(metric)
        return dict(
            timestamp=str(datetime.now()),
            metrics=metrics_dicts,
        )

    def _build_dashboard_info(self):
        metrics_results = []
        additional_graphs = []
        for test in self._first_level_metrics:
            renderer = find_metric_renderer(type(test), self._inner_suite.context.renderers)
            html_info = renderer.render_html(test)
            for info_item in html_info:
                for additional_graph in info_item.get_additional_graphs():
                    if isinstance(additional_graph, AdditionalGraphInfo):
                        additional_graphs.append(DetailsInfo("", additional_graph.params, additional_graph.id))
                    else:
                        additional_graphs.append(DetailsInfo("", additional_graph, additional_graph.id))
            metrics_results.extend(html_info)

        return (
            "evidently_dashboard_" + str(uuid.uuid4()).replace("-", ""),
            DashboardInfo("Report", widgets=[result for result in metrics_results]),
            {
                f"{item.id}": dataclasses.asdict(item.info) if dataclasses.is_dataclass(item.info) else item.info
                for item in additional_graphs
            },
        )
