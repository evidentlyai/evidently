from evidently.metrics.base_metric import InputData
from evidently.test_preset.test_preset import TestPreset
from evidently.tests import (TestAllColumnsShareOfNulls,
                             TestCatColumnsOutOfListValues, TestColumnsType,
                             TestNumberOfColumns, TestNumberOfRows,
                             TestNumColumnsMeanInNSigmas,
                             TestNumColumnsOutOfRangeValues)
from evidently.utils.data_operations import DatasetColumns


class DataStability(TestPreset):
    def generate_tests(self, data: InputData, columns: DatasetColumns):
        return [
            TestNumberOfRows(),
            TestNumberOfColumns(),
            TestColumnsType(),
            TestAllColumnsShareOfNulls(),
            TestNumColumnsOutOfRangeValues(),
            TestCatColumnsOutOfListValues(),
            TestNumColumnsMeanInNSigmas(),
        ]
