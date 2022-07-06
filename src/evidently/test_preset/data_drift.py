from evidently.analyzers.utils import DatasetColumns
from evidently.metrics.base_metric import InputData
from evidently.test_preset.test_preset import TestPreset
from evidently.tests import TestFeatureValueDrift
from evidently.tests import TestShareOfDriftedFeatures


class DataDrift(TestPreset):
    def generate_tests(self, data: InputData, columns: DatasetColumns):
        preset_tests: list = [TestShareOfDriftedFeatures()]

        if columns.utility_columns.target is not None:
            preset_tests.append(TestFeatureValueDrift(column_name=columns.utility_columns.target))

        if columns.utility_columns.prediction is not None and isinstance(columns.utility_columns.prediction, str):
            preset_tests.append(TestFeatureValueDrift(column_name=columns.utility_columns.prediction))

        for name in columns.num_feature_names + columns.cat_feature_names:
            if name is not None:
                preset_tests.append(TestFeatureValueDrift(column_name=name))

        return preset_tests
