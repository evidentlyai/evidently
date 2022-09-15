import dataclasses
import uuid
from datetime import datetime
from typing import List
from typing import Optional
from typing import Union

import pandas as pd

from evidently import ColumnMapping
from evidently.metric_preset.metric_preset import MetricPreset
from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.model.dashboard import DashboardInfo
from evidently.suite.base_suite import Display
from evidently.suite.base_suite import Suite
from evidently.suite.base_suite import find_metric_renderer
from evidently.utils.data_operations import DatasetColumns
from evidently.utils.data_operations import process_columns


class Report(Display):
    _inner_suite: Suite
    _columns_info: DatasetColumns
    _first_level_metrics: List[Union[Metric]]
    metrics: List[Union[Metric, MetricPreset]]

    def __init__(self, metrics: List[Union[Metric, MetricPreset]]):
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
            if isinstance(item, MetricPreset):
                metrics = item.generate_metrics(data=data, columns=self._columns_info)

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
        for test, _ in self._inner_suite.context.metric_results.items():
            renderer = find_metric_renderer(type(test), self._inner_suite.context.renderers)
            metrics_results.extend(renderer.render_html(test))

        return (
            "evidently_dashboard_" + str(uuid.uuid4()).replace("-", ""),
            DashboardInfo("Report", widgets=[result.info for result in metrics_results]),
            {
                f"{item.id}": dataclasses.asdict(item.info)
                for idx, info in enumerate(metrics_results)
                for item in info.details
            },
        )
