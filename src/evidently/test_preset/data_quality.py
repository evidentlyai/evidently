from evidently.metrics.base_metric import InputData
from evidently.test_preset.test_preset import TestPreset
from evidently.tests import (TestAllColumnsMostCommonValueShare,
                             TestAllColumnsShareOfNulls,
                             TestHighlyCorrelatedFeatures,
                             TestNumberOfConstantColumns,
                             TestNumberOfDuplicatedColumns,
                             TestNumberOfDuplicatedRows)
from evidently.utils.data_operations import DatasetColumns


class DataQuality(TestPreset):
    def generate_tests(self, data: InputData, columns: DatasetColumns):
        return [
            TestAllColumnsShareOfNulls(),
            TestAllColumnsMostCommonValueShare(),
            TestNumberOfConstantColumns(),
            TestNumberOfDuplicatedColumns(),
            TestNumberOfDuplicatedRows(),
            TestHighlyCorrelatedFeatures(),
        ]
