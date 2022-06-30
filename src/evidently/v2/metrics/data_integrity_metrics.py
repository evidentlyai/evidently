from dataclasses import dataclass
from itertools import combinations

from evidently.v2.metrics.base_metric import InputData
from evidently.v2.metrics.base_metric import Metric


@dataclass
class DataIntegrityMetricsResults:
    number_of_columns: int
    number_of_rows: int
    number_of_nans: int
    number_of_columns_with_nans: int
    number_of_rows_with_nans: int
    # number_of_differently_encoded_nulls: int
    number_of_constant_columns: int
    number_of_empty_rows: int
    number_of_empty_columns: int
    number_of_duplicated_rows: int
    number_of_duplicated_columns: int
    columns_type: dict
    nans_by_columns: dict
    number_uniques_by_columns: dict


class DataIntegrityMetrics(Metric[DataIntegrityMetricsResults]):
    def calculate(self, data: InputData, metrics: dict) -> DataIntegrityMetricsResults:
        return DataIntegrityMetricsResults(
            number_of_columns=len(data.current_data.columns),
            number_of_rows=data.current_data.shape[0],
            number_of_nans=data.current_data.isna().sum().sum(),
            number_of_columns_with_nans=data.current_data.isna().any().sum(),
            number_of_rows_with_nans=data.current_data.isna().any(axis=1).sum(),
            number_of_constant_columns=len(data.current_data.columns[data.current_data.nunique() <= 1]),  # type: ignore
            number_of_empty_rows=data.current_data.isna().all(1).sum(),
            number_of_empty_columns=data.current_data.isna().all().sum(),
            number_of_duplicated_rows=data.current_data.duplicated().sum(),
            number_of_duplicated_columns=sum([
                1 for i, j in combinations(data.current_data, 2) if data.current_data[i].equals(data.current_data[j])
            ]),
            columns_type=dict(data.current_data.dtypes.to_dict()),
            nans_by_columns=data.current_data.isna().sum().to_dict(),
            number_uniques_by_columns=dict(data.current_data.nunique().to_dict())
        )
