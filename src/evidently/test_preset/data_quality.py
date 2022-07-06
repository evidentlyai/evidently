from typing import List

from evidently.analyzers.utils import DatasetColumns
from evidently.metrics.base_metric import InputData
from evidently.test_preset.test_preset import TestPreset
from evidently.tests import TestColumnNANShare
from evidently.tests import TestMostCommonValueShare
from evidently.tests import TestNumberOfConstantColumns
from evidently.tests import TestNumberOfDuplicatedColumns
from evidently.tests import TestNumberOfDuplicatedRows
from evidently.tests import TestHighlyCorrelatedFeatures


class DataQuality(TestPreset):
    def generate_tests(self, data: InputData, columns: DatasetColumns):
        all_columns: List[str] = columns.get_all_columns_list()
        return [
            *[TestColumnNANShare(column_name=name) for name in all_columns],
            *[TestMostCommonValueShare(column_name=name) for name in all_columns],
            TestNumberOfConstantColumns(),
            TestNumberOfDuplicatedColumns(),
            TestNumberOfDuplicatedRows(),
            TestHighlyCorrelatedFeatures(),
        ]
