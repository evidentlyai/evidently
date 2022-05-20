from dataclasses import dataclass
from typing import List
from evidently.suites.metrics.base_metrics import SourceOneDatasetAnalyzer


@dataclass
class DatasetMetadataMetricResult:
    all_rows_count: int
    features_count: int
    column_names: List[str]


class DatasetMetadataMetric(SourceOneDatasetAnalyzer):
    name = "dataset_metadata_metrics"
    description = "Quantity of all row in the dataset, with NaN values"
    result: DatasetMetadataMetricResult

    def calculate(self):
        all_rows_count = len(self.dataset)
        features_count = len(self.dataset.columns)
        column_names = list(self.dataset.columns)
        return DatasetMetadataMetricResult(
            all_rows_count=all_rows_count,
            features_count=features_count,
            column_names=column_names
        )
