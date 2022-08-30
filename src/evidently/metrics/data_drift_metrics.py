import dataclasses
from typing import Dict
from typing import List
from typing import Optional
from dataclasses import dataclass

import pandas as pd

from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.calculations.data_drift import get_overall_data_drift
from evidently.calculations.data_drift import DataDriftAnalyzerMetrics
from evidently.metrics.utils import make_hist_for_num_plot
from evidently.metrics.utils import make_hist_for_cat_plot
from evidently.model.widget import BaseWidgetInfo
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.base_renderer import MetricHtmlInfo
from evidently.renderers.base_renderer import MetricRenderer
from evidently.options import DataDriftOptions
from evidently.options import OptionsProvider
from evidently.utils.data_operations import process_columns


@dataclass
class DataDriftMetricsResults:
    options: DataDriftOptions
    metrics: DataDriftAnalyzerMetrics
    distr_for_plots: Dict[str, Dict[str, pd.DataFrame]]


class DataDriftMetrics(Metric[DataDriftMetricsResults]):
    options: Optional[DataDriftOptions]

    def __init__(self, options: Optional[DataDriftOptions] = None):
        self.options = options

    def get_parameters(self) -> tuple:
        return tuple((self.options,))

    def calculate(self, data: InputData) -> DataDriftMetricsResults:
        columns = process_columns(data.current_data, data.column_mapping)
        options_provider: OptionsProvider = OptionsProvider()

        if self.options is not None:
            options_provider.add(self.options)

        options = options_provider.get(DataDriftOptions)

        if data.reference_data is None:
            raise ValueError("Reference dataset should be present")

        drift_metrics = get_overall_data_drift(
            current_data=data.current_data,
            reference_data=data.reference_data,
            columns=columns,
            data_drift_options=options,
        )
        distr_for_plots = {}

        for feature in columns.num_feature_names:
            distr_for_plots[feature] = make_hist_for_num_plot(data.current_data[feature], data.reference_data[feature])

        for feature in columns.cat_feature_names:
            distr_for_plots[feature] = make_hist_for_cat_plot(data.current_data[feature], data.reference_data[feature])

        return DataDriftMetricsResults(options=options, metrics=drift_metrics, distr_for_plots=distr_for_plots)


@default_renderer(wrap_type=DataDriftMetrics)
class TestNumberOfDriftedFeaturesRenderer(MetricRenderer):
    def render_json(self, obj: DataDriftMetrics) -> dict:
        return dataclasses.asdict(obj.get_result().metrics)

    def render_html(self, obj: DataDriftMetrics) -> List[MetricHtmlInfo]:
        return [
            MetricHtmlInfo(
                "data_drift",
                BaseWidgetInfo(
                    type="counter",
                    title="Data Drift",
                    size=2,
                    params={
                        "counters": [
                            {"value": "", "label": f"Share:'{obj.get_result().metrics.share_drifted_features}'"}
                        ]
                    },
                ),
                details=[],
            ),
        ]
