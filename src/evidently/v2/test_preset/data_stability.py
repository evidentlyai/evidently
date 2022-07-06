from typing import List

from evidently.analyzers.utils import DatasetColumns
from evidently.v2.metrics.base_metric import InputData
from evidently.v2.test_preset.test_preset import TestPreset
from evidently.v2.tests import TestNumberOfRows
from evidently.v2.tests import TestNumberOfColumns
from evidently.v2.tests import TestColumnsType
from evidently.v2.tests import TestColumnNANShare
from evidently.v2.tests import TestShareOfOutRangeValues
from evidently.v2.tests import TestShareOfOutListValues
from evidently.v2.tests import TestMeanInNSigmas


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
