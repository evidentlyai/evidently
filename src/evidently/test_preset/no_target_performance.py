from typing import List
from typing import Optional

from evidently.metrics.base_metric import InputData
from evidently.test_preset.test_preset import TestPreset
from evidently.tests import TestAllColumnsShareOfNulls
from evidently.tests import TestCatColumnsOutOfListValues
from evidently.tests import TestColumnsType
from evidently.tests import TestColumnValueDrift
from evidently.tests import TestCustomFeaturesValueDrift
from evidently.tests import TestNumColumnsMeanInNSigmas
from evidently.tests import TestNumColumnsOutOfRangeValues
from evidently.tests import TestShareOfDriftedColumns
from evidently.utils.data_operations import DatasetColumns


class NoTargetPerformanceTestPreset(TestPreset):
    columns: List[str]

    def __init__(self, columns: Optional[List[str]] = None):
        super().__init__()
        self.columns = [] if columns is None else columns

    def generate_tests(self, data: InputData, columns: DatasetColumns):
        preset_tests: List = []

        if columns.utility_columns.prediction is not None and isinstance(columns.utility_columns.prediction, str):
            preset_tests.append(TestColumnValueDrift(column_name=columns.utility_columns.prediction))

        preset_tests.append(TestShareOfDriftedColumns(lt=data.current_data.shape[1] // 3))
        preset_tests.append(TestColumnsType())
        preset_tests.append(TestAllColumnsShareOfNulls())
        preset_tests.append(TestNumColumnsOutOfRangeValues())
        preset_tests.append(TestCatColumnsOutOfListValues())
        preset_tests.append(TestNumColumnsMeanInNSigmas())

        if self.columns:
            preset_tests.append(TestCustomFeaturesValueDrift(features=self.columns))

        return preset_tests
