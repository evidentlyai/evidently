from typing import Dict
from typing import Optional
from dataclasses import dataclass

import pandas as pd

from evidently.analyzers.data_drift_analyzer import DataDriftAnalyzer
from evidently.analyzers.data_drift_analyzer import DataDriftAnalyzerResults
from evidently.options import DataDriftOptions
from evidently.options import OptionsProvider

from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.metrics.utils import make_hist_for_num_plot
from evidently.metrics.utils import make_hist_for_cat_plot


@dataclass
class DataDriftMetricsResults:
    analyzer_result: DataDriftAnalyzerResults
    distr_for_plots: Dict[str, Dict[str, pd.DataFrame]]


class DataDriftMetrics(Metric[DataDriftMetricsResults]):
    def __init__(self, options: Optional[DataDriftOptions] = None):
        self.analyzer = DataDriftAnalyzer()
        self.analyzer.options_provider = OptionsProvider()

        if options is not None:
            self.analyzer.options_provider.add(options)

    def calculate(self, data: InputData, metrics: dict) -> DataDriftMetricsResults:
        if data.reference_data is None:
            raise ValueError("Reference dataset should be present")

        analyzer_result = self.analyzer.calculate(data.reference_data, data.current_data, data.column_mapping)
        distr_for_plots = {}
        for feature in analyzer_result.columns.num_feature_names:
            distr_for_plots[feature] = make_hist_for_num_plot(data.current_data[feature], data.reference_data[feature])
        for feature in analyzer_result.columns.cat_feature_names:
            distr_for_plots[feature] = make_hist_for_cat_plot(data.current_data[feature], data.reference_data[feature])

        return DataDriftMetricsResults(analyzer_result=analyzer_result, distr_for_plots=distr_for_plots)
