from typing import Dict
from typing import Optional
from dataclasses import dataclass

import pandas as pd

from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.calculations.data_drift import DataDriftAnalyzerMetrics
from evidently.metrics.utils import make_hist_for_num_plot
from evidently.metrics.utils import make_hist_for_cat_plot
from evidently.options import DataDriftOptions
from evidently.options import OptionsProvider


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

    def calculate(self, data: InputData, metrics: dict) -> DataDriftMetricsResults:
        from evidently.analyzers.data_drift_analyzer import DataDriftAnalyzer

        analyzer = DataDriftAnalyzer()
        analyzer.options_provider = OptionsProvider()
        if self.options is not None:
            analyzer.options_provider.add(self.options)

        if data.reference_data is None:
            raise ValueError("Reference dataset should be present")

        analyzer_result = analyzer.calculate(data.reference_data, data.current_data, data.column_mapping)
        distr_for_plots = {}
        for feature in analyzer_result.columns.num_feature_names:
            distr_for_plots[feature] = make_hist_for_num_plot(data.current_data[feature], data.reference_data[feature])
        for feature in analyzer_result.columns.cat_feature_names:
            distr_for_plots[feature] = make_hist_for_cat_plot(data.current_data[feature], data.reference_data[feature])

        return DataDriftMetricsResults(
            options=analyzer_result.options, metrics=analyzer_result.metrics, distr_for_plots=distr_for_plots
        )
