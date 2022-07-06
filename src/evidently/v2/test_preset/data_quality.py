from typing import List

from evidently.analyzers.utils import DatasetColumns
from evidently.v2.metrics.base_metric import InputData
from evidently.v2.test_preset.test_preset import TestPreset
from evidently.v2.tests import TestColumnNANShare
from evidently.v2.tests import TestMostCommonValueShare
from evidently.v2.tests import TestNumberOfConstantColumns
from evidently.v2.tests import TestNumberOfDuplicatedColumns
from evidently.v2.tests import TestNumberOfDuplicatedRows
from evidently.v2.tests import TestHighlyCorrelatedFeatures


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
