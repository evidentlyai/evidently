from evidently.analyzers.utils import DatasetColumns
from evidently.v2.metrics.base_metric import InputData
from evidently.v2.test_preset.test_preset import TestPreset
from evidently.v2.tests import TestColumnNANShare, TestMostCommonValueShare, TestNumberOfConstantColumns, \
    TestNumberOfDuplicatedColumns, TestNumberOfDuplicatedRows
from evidently.v2.tests.data_quality_tests import HighlyCorrelatedFeatures


class DataQuality(TestPreset):
    def generate_tests(self, data: InputData, columns: DatasetColumns):
        all_columns = [name for name in columns.cat_feature_names + columns.num_feature_names + [
            columns.utility_columns.id_column,
            columns.utility_columns.date,
            columns.utility_columns.target,
            columns.utility_columns.prediction,
        ] if name is not None]
        return [
            *[TestColumnNANShare(column_name=name) for name in all_columns],
            *[TestMostCommonValueShare(column_name=name) for name in all_columns],
            TestNumberOfConstantColumns(),
            TestNumberOfDuplicatedColumns(),
            TestNumberOfDuplicatedRows(),
            HighlyCorrelatedFeatures(),
        ]
