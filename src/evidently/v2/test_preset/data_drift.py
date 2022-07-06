from evidently.analyzers.utils import DatasetColumns
from evidently.v2.metrics.base_metric import InputData
from evidently.v2.test_preset.test_preset import TestPreset
from evidently.v2.tests import TestShareOfDriftedFeatures, TestFeatureValueDrift


class DataDrift(TestPreset):
    def generate_tests(self, data: InputData, columns: DatasetColumns):
        return [
            TestShareOfDriftedFeatures(),
            TestFeatureValueDrift(column_name=columns.utility_columns.target),
            TestFeatureValueDrift(column_name=columns.utility_columns.prediction),
            *[
                TestFeatureValueDrift(column_name=name)
                for name in columns.num_feature_names + columns.cat_feature_names
                if name is not None
            ],
        ]
