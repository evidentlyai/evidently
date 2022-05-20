from dataclasses import dataclass
from typing import Optional
from evidently.suites.metrics.base_metrics import BaseTest
from evidently.suites.metrics.base_metrics import SourceOneDatasetAnalyzer
from evidently.suites.metrics.source_metadata_metrics import DatasetMetadataMetric


@dataclass
class TestNumber(BaseTest):
    required_analyzer = SourceOneDatasetAnalyzer
    calculated_analyzer: Optional[SourceOneDatasetAnalyzer] = None

    exact: Optional[int] = None
    gt: Optional[int] = None
    lt: Optional[int] = None

    value: Optional[int] = None

    def set_value(self):
        raise NotImplemented

    def calculate(self) -> bool:
        result = False

        self.set_value()

        if self.exact is not None:
            result = self.value == self.exact

        if self.gt is not None:
            result = self.value > self.gt

        if self.exact is not None:
            result = self.value < self.lt

        return result

    def get_details(self) -> str:
        conditions = []
        if self.exact:
            conditions.append(f"x equals {self.exact}")

        if self.gt:
            conditions.append(f"x is greater than {self.gt}")

        if self.lt:
            conditions.append(f"x is less than {self.lt}")

        if conditions:
            conditions = ", ".join(conditions)

        else:
            conditions = "no conditions"

        return f"Value {self.value} was compared with {conditions}"


@dataclass
class TestNumberOfRows(TestNumber):
    name: str = "test_number_of_rows"
    description: str = "Check how many rows in the dataset. Including rows with NaN values."
    required_analyzer = DatasetMetadataMetric
    calculated_analyzer: Optional[DatasetMetadataMetric] = None

    def set_value(self):
        self.value = self.calculated_analyzer.result.all_rows_count


@dataclass
class TestNumberOfFeatures(TestNumber):
    name: str = "test_number_of_features"
    description: str = "Check how many features in the dataset."
    required_analyzer = DatasetMetadataMetric
    calculated_analyzer: Optional[DatasetMetadataMetric] = None

    def set_value(self):
        self.value = self.calculated_analyzer.result.features_count


class TestIsTargetPresented(BaseTest):
    name: str = "test_is_target_in_dataset"
    description: str = "Check that target is presented in the dataset."
    required_analyzer = DatasetMetadataMetric
    calculated_analyzer: DatasetMetadataMetric

    def calculate(self) -> bool:
        return "target" in self.calculated_analyzer.result.column_names

    def get_details(self) -> str:
        return f"Search target in {self.calculated_analyzer.result.column_names}"
