from dataclasses import dataclass

from .base_metric import Metric, InputData


@dataclass
class DataIntegrityMetricsResults:
    number_of_columns: int
    number_of_rows: int
    number_of_nulls: int
    number_of_columns_with_nulls: int
    number_of_rows_with_nulls: int
    number_of_differently_encoded_nulls: int
    number_of_constant_columns: int
    number_of_empty_rows: int
    number_of_empty_columns: int
    number_of_duplicated_rows: int
    number_of_duplicated_columns: int


class DataIntegrityMetrics(Metric[DataIntegrityMetricsResults]):
    def calculate(self, data: InputData, metrics: dict) -> DataIntegrityMetricsResults:
        return DataIntegrityMetricsResults(
            number_of_columns=len(data.current_data.columns),
            number_of_rows=data.current_data.shape[0],
            number_of_nulls=data.current_data.isna().sum().sum(),
            # TODO: implement the follow metrics calculation
            number_of_columns_with_nulls=0,
            number_of_rows_with_nulls=0,
            number_of_differently_encoded_nulls=0,
            number_of_constant_columns=0,
            number_of_empty_rows=0,
            number_of_empty_columns=0,
            number_of_duplicated_rows=0,
            number_of_duplicated_columns=0
        )
