from dataclasses import dataclass

from .base_metric import Metric, InputData


@dataclass
class DataIntegrityMetricsResults:
    number_of_columns: int


class DataIntegrityMetrics(Metric[DataIntegrityMetricsResults]):
    def calculate(self, data: InputData, metrics: dict) -> DataIntegrityMetricsResults:
        return DataIntegrityMetricsResults(
            number_of_columns=len(data.current_data.columns)
        )