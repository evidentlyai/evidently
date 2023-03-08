from typing import List, Optional

from evidently.base_metric import InputData
from evidently.test_preset.test_preset import TestPreset
from evidently.tests import (
    TestAllColumnsShareOfMissingValues,
    TestCatColumnsOutOfListValues,
    TestColumnsType,
    TestNumberOfColumns,
    TestNumberOfRows,
    TestNumColumnsMeanInNSigmas,
    TestNumColumnsOutOfRangeValues,
)
from evidently.utils.data_operations import DatasetColumns


class DataStabilityTestPreset(TestPreset):
    """
    Data Stability tests.

    Contains tests:
    - `TestNumberOfRows`
    - `TestNumberOfColumns`
    - `TestColumnsType`
    - `TestAllColumnsShareOfMissingValues`
    - `TestNumColumnsOutOfRangeValues`
    - `TestCatColumnsOutOfListValues`
    - `TestNumColumnsMeanInNSigmas`
    """

    columns: Optional[List[str]]

    def __init__(
        self,
        columns: Optional[List[str]] = None,
    ):
        super().__init__()
        self.columns = columns

    def generate_tests(self, data: InputData, columns: DatasetColumns):
        return [
            TestNumberOfRows(),
            TestNumberOfColumns(),
            TestColumnsType(),
            TestAllColumnsShareOfMissingValues(columns=self.columns),
            TestNumColumnsOutOfRangeValues(columns=self.columns),
            TestCatColumnsOutOfListValues(columns=self.columns),
            TestNumColumnsMeanInNSigmas(columns=self.columns),
        ]
