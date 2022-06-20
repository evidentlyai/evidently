from evidently.analyzers.data_drift_analyzer import DataDriftAnalyzer, DataDriftAnalyzerResults
from evidently.options import OptionsProvider, DataDriftOptions
from evidently.v2.metrics.base_metric import Metric, InputData


class DataDriftResults(DataDriftAnalyzerResults):
    pass


class DataDriftMetrics(Metric[DataDriftResults]):
    def __init__(self, options: DataDriftOptions = None):
        self.analyzer = DataDriftAnalyzer()
        self.analyzer.options_provider = OptionsProvider()
        if options is not None:
            self.analyzer.options_provider.add(options)

    def calculate(self, data: InputData, metrics: dict):
        results = self.analyzer.calculate(data.reference_data, data.current_data, data.column_mapping)
        return results
