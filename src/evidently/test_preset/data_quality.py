from evidently.metrics.base_metric import InputData
from evidently.test_preset.test_preset import TestPreset
from evidently.tests import TestAllColumnsMostCommonValueShare
from evidently.tests import TestAllColumnsShareOfNulls
from evidently.tests import TestHighlyCorrelatedColumns
from evidently.tests import TestNumberOfConstantColumns
from evidently.tests import TestNumberOfDuplicatedColumns
from evidently.tests import TestNumberOfDuplicatedRows
from evidently.utils.data_operations import DatasetColumns


class DataQualityTestPreset(TestPreset):
    def generate_tests(self, data: InputData, columns: DatasetColumns):
        return [
            TestAllColumnsShareOfNulls(),
            TestAllColumnsMostCommonValueShare(),
            TestNumberOfConstantColumns(),
            TestNumberOfDuplicatedColumns(),
            TestNumberOfDuplicatedRows(),
            TestHighlyCorrelatedColumns(),
        ]
