from typing import List

from evidently.analyzers.utils import DatasetColumns
from evidently.metrics.base_metric import InputData
from evidently.test_preset.test_preset import TestPreset
from evidently.tests import TestNumberOfRows
from evidently.tests import TestNumberOfColumns
from evidently.tests import TestColumnsType
from evidently.tests import TestColumnNANShare
from evidently.tests import TestShareOfOutRangeValues
from evidently.tests import TestShareOfOutListValues
from evidently.tests import TestMeanInNSigmas


class DataStability(TestPreset):
    def generate_tests(self, data: InputData, columns: DatasetColumns):
        all_columns: List[str] = columns.get_all_columns_list()
        return [
            TestNumberOfRows(),
            TestNumberOfColumns(),
            TestColumnsType(),
            *[TestColumnNANShare(column_name=name) for name in all_columns],
            *[TestShareOfOutRangeValues(column_name=name) for name in columns.num_feature_names],
            *[TestShareOfOutListValues(column_name=name) for name in columns.cat_feature_names],
            *[TestMeanInNSigmas(column_name=name, n_sigmas=2) for name in columns.num_feature_names],
        ]
