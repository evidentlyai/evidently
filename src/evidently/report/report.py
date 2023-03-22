import dataclasses
import uuid
from collections import defaultdict
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import pandas as pd

from evidently import ColumnMapping
from evidently.base_metric import InputData
from evidently.base_metric import Metric
from evidently.metric_preset.metric_preset import MetricPreset
from evidently.metric_results import DatasetColumns
from evidently.model.dashboard import DashboardInfo
from evidently.model.widget import AdditionalGraphInfo
from evidently.options import ColorOptions
from evidently.renderers.base_renderer import DetailsInfo
from evidently.suite.base_suite import Display
from evidently.suite.base_suite import Suite
from evidently.suite.base_suite import find_metric_renderer
from evidently.utils.data_operations import process_columns
from evidently.utils.data_preprocessing import create_data_definition
from evidently.utils.generators import BaseGenerator


class Report(Display):
    _inner_suite: Suite
    _columns_info: DatasetColumns
    _first_level_metrics: List[Union[Metric]]
    metrics: List[Union[Metric, MetricPreset, BaseGenerator]]

    def __init__(self, metrics: List[Union[Metric, MetricPreset, BaseGenerator]], options: Optional[List] = None):
        super().__init__(options)
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

        self._inner_suite.verify()

        data_definition = create_data_definition(reference_data, current_data, column_mapping)
        data = InputData(reference_data, current_data, None, None, column_mapping, data_definition)

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

        data_definition = create_data_definition(reference_data, current_data, column_mapping)
        curr_add, ref_add = self._inner_suite.create_additional_features(current_data, reference_data, data_definition)
        data = InputData(
            reference_data,
            current_data,
            ref_add,
            curr_add,
            column_mapping,
            data_definition,
        )
        self._inner_suite.run_calculate(data)

    def as_dict(self) -> dict:
        metrics = []

        for metric in self._first_level_metrics:
            renderer = find_metric_renderer(type(metric), self._inner_suite.context.renderers)
            metrics.append({"metric": metric.get_id(), "result": renderer.render_json(metric)})

        return {
            "metrics": metrics,
        }

    def as_pandas(self, group: str = None) -> Union[Dict[str, pd.DataFrame], pd.DataFrame]:
        metrics = defaultdict(list)

        for metric in self._first_level_metrics:
            renderer = find_metric_renderer(type(metric), self._inner_suite.context.renderers)
            metric_id = metric.get_id()
            if group is not None and metric_id != group:
                continue
            metrics[metric_id].append(renderer.render_pandas(metric))

        result = {cls: pd.concat(val) for cls, val in metrics.items()}
        if group is None and len(result) == 1:
            return next(iter(result.values()))
        if group is None:
            return result
        if group not in result:
            raise ValueError(f"Metric group {group} not found in this report")
        return result[group]

    def _build_dashboard_info(self):
        metrics_results = []
        additional_graphs = []

        color_options = self.options_provider.get(ColorOptions)

        for test in self._first_level_metrics:
            renderer = find_metric_renderer(type(test), self._inner_suite.context.renderers)
            # set the color scheme from the report for each render
            renderer.color_options = color_options
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
