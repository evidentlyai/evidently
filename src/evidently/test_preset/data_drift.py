from evidently.metrics.base_metric import InputData
from evidently.test_preset.test_preset import TestPreset
from evidently.tests import TestAllFeaturesValueDrift
from evidently.tests import TestColumnValueDrift
from evidently.tests import TestShareOfDriftedColumns
from evidently.utils.data_operations import DatasetColumns


class DataDriftTestPreset(TestPreset):
    def generate_tests(self, data: InputData, columns: DatasetColumns):
        preset_tests: list = [TestShareOfDriftedColumns()]

        if columns.utility_columns.target is not None:
            preset_tests.append(TestColumnValueDrift(column_name=columns.utility_columns.target))

        if columns.utility_columns.prediction is not None and isinstance(columns.utility_columns.prediction, str):
            preset_tests.append(TestColumnValueDrift(column_name=columns.utility_columns.prediction))

        preset_tests.append(TestAllFeaturesValueDrift())

        return preset_tests
