from evidently.analyzers.utils import DatasetColumns
from evidently.v2.metrics.base_metric import InputData
from evidently.v2.test_preset.test_preset import TestPreset
from evidently.v2.tests import TestNumberOfRows, TestNumberOfColumns, TestColumnsType, TestColumnNANShare, \
    TestShareOfOutRangeValues, TestShareOfOutListValues, TestMeanInNSigmas


class DataStability(TestPreset):
    def generate_tests(self, data: InputData, columns: DatasetColumns):
        all_columns = [name for name in columns.cat_feature_names + columns.num_feature_names + [
            columns.utility_columns.id_column,
            columns.utility_columns.date,
            columns.utility_columns.target,
            columns.utility_columns.prediction,
        ] if name is not None]
        return [
            TestNumberOfRows(),
            TestNumberOfColumns(),
            TestColumnsType(),
            *[TestColumnNANShare(column_name=name) for name in all_columns],
            *[TestShareOfOutRangeValues(column_name=name) for name in columns.num_feature_names],
            *[TestShareOfOutListValues(column_name=name) for name in columns.cat_feature_names],
            *[TestMeanInNSigmas(column_name=name, n_sigmas=2) for name in columns.num_feature_names],
        ]
