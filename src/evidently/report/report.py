import dataclasses
import uuid
from typing import List
from typing import Optional
from typing import Union

import pandas as pd

from evidently import ColumnMapping
from evidently.dashboard.dashboard import TemplateParams
from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.model.dashboard import DashboardInfo
from evidently.renderers.notebook_utils import determine_template
from evidently.suite.base_suite import find_metric_renderer
from evidently.suite.base_suite import Suite
from evidently.utils.data_operations import process_columns
from evidently.utils.data_operations import DatasetColumns


class Report:
    _inner_suite: Suite
    _columns_info: DatasetColumns

    def __init__(self, metrics: List[Union[Metric]]):
        super().__init__()
        self.metrics = metrics
        self._inner_suite = Suite()

    def run(
        self,
        *,
        reference_data: Optional[pd.DataFrame],
        current_data: pd.DataFrame,
        column_mapping: Optional[ColumnMapping] = None,
    ) -> None:
        if column_mapping is None:
            column_mapping = ColumnMapping()
        self._columns_info = process_columns(current_data, column_mapping)
        for metric in self.metrics:
            self._inner_suite.add_metric(metric)
        self._inner_suite.verify()
        self._inner_suite.run_calculate(InputData(reference_data, current_data, column_mapping))

    def _repr_html_(self):
        dashboard_id, dashboard_info, graphs = self._build_dashboard_info()
        template_params = TemplateParams(
            dashboard_id=dashboard_id, dashboard_info=dashboard_info, additional_graphs=graphs
        )
        return self._render(determine_template("auto"), template_params)

    def _render(self, temple_func, template_params: TemplateParams):
        return temple_func(params=template_params)

    def _build_dashboard_info(self):
        metrics_results = []
        for test, _ in self._inner_suite.context.metric_results.items():
            renderer = find_metric_renderer(type(test), self._inner_suite.context.renderers)
            metrics_results.extend(renderer.render_html(test))

        return (
            "evidently_dashboard_" + str(uuid.uuid4()).replace("-", ""),
            DashboardInfo("Report", widgets=[result.info for result in metrics_results]),
            {
                f"{info.name}_{idx}_{item.id}": dataclasses.asdict(item.info)
                for idx, info in enumerate(metrics_results)
                for item in info.details
            },
        )
