from evidently.analyzers.data_drift_analyzer import DataDriftAnalyzer
from evidently.analyzers.data_drift_analyzer import DataDriftAnalyzerResults
from evidently.options import DataDriftOptions
from evidently.options import OptionsProvider

from evidently.v2.metrics.base_metric import InputData
from evidently.v2.metrics.base_metric import Metric


DataDriftMetricsResults = DataDriftAnalyzerResults


class DataDriftMetrics(Metric[DataDriftMetricsResults]):
    def __init__(self, options: DataDriftOptions = None):
        self.analyzer = DataDriftAnalyzer()
        self.analyzer.options_provider = OptionsProvider()

        if options is not None:
            self.analyzer.options_provider.add(options)

    def calculate(self, data: InputData, metrics: dict) -> DataDriftMetricsResults:
        results = self.analyzer.calculate(data.reference_data, data.current_data, data.column_mapping)
        return results
