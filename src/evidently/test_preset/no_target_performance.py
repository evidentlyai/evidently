from typing import List
from typing import Optional

from evidently.analyzers.utils import DatasetColumns
from evidently.metrics.base_metric import InputData
from evidently.test_preset.test_preset import TestPreset
from evidently.tests import TestFeatureValueDrift
from evidently.tests import TestShareOfDriftedFeatures
from evidently.tests import TestColumnNANShare
from evidently.tests import TestShareOfOutRangeValues
from evidently.tests import TestShareOfOutListValues
from evidently.tests import TestMeanInNSigmas
from evidently.tests import TestColumnsType


class NoTargetPerformance(TestPreset):
    def __init__(self, most_important_features: Optional[List[str]] = None):
        super().__init__()
        self.most_important_features = [] if most_important_features is None else most_important_features

    def generate_tests(self, data: InputData, columns: DatasetColumns):
        all_columns: List[str] = columns.get_all_columns_list()
        preset_tests: List = []

        if columns.utility_columns.prediction is not None and isinstance(columns.utility_columns.prediction, str):
            preset_tests.append(TestFeatureValueDrift(column_name=columns.utility_columns.prediction))

        preset_tests.append(TestShareOfDriftedFeatures(lt=data.current_data.shape[1] // 3))
        preset_tests.append(TestColumnsType())
        preset_tests.extend([TestColumnNANShare(column_name=name) for name in all_columns])
        preset_tests.extend([TestShareOfOutRangeValues(column_name=name) for name in columns.num_feature_names])
        preset_tests.extend([TestShareOfOutListValues(column_name=name) for name in columns.cat_feature_names])
        preset_tests.extend([TestMeanInNSigmas(column_name=name, n_sigmas=2) for name in columns.num_feature_names])
        preset_tests.extend([TestFeatureValueDrift(column_name=name) for name in self.most_important_features])
        return preset_tests
