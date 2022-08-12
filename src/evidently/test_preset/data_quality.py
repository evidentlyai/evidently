from typing import List

from evidently.analyzers.utils import DatasetColumns
from evidently.metrics.base_metric import InputData
from evidently.test_preset.test_preset import TestPreset
from evidently.tests import TestColumnShareOfNulls
from evidently.tests import TestAllColumnsMostCommonValueShare
from evidently.tests import TestNumberOfConstantColumns
from evidently.tests import TestNumberOfDuplicatedColumns
from evidently.tests import TestNumberOfDuplicatedRows
from evidently.tests import TestHighlyCorrelatedFeatures


class DataQuality(TestPreset):
    def generate_tests(self, data: InputData, columns: DatasetColumns):
        return [
            TestColumnShareOfNulls(),
            TestAllColumnsMostCommonValueShare(),
            TestNumberOfConstantColumns(),
            TestNumberOfDuplicatedColumns(),
            TestNumberOfDuplicatedRows(),
            TestHighlyCorrelatedFeatures(),
        ]
