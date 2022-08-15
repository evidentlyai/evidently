from typing import List
from typing import Optional

from evidently.analyzers.utils import DatasetColumns
from evidently.metrics.base_metric import InputData
from evidently.test_preset.test_preset import TestPreset
from evidently.tests import TestFeatureValueDrift
from evidently.tests import TestShareOfDriftedFeatures
from evidently.tests import TestAllColumnsShareOfNulls
from evidently.tests import TestNumColumnsOutOfRangeValues
from evidently.tests import TestCatColumnsOutOfListValues
from evidently.tests import TestNumColumnsMeanInNSigmas
from evidently.tests import TestCustomFeaturesValueDrift
from evidently.tests import TestColumnsType


class NoTargetPerformance(TestPreset):
    def __init__(self, most_important_features: Optional[List[str]] = None):
        super().__init__()
        self.most_important_features = [] if most_important_features is None else most_important_features

    def generate_tests(self, data: InputData, columns: DatasetColumns):
        preset_tests: List = []

        if columns.utility_columns.prediction is not None and isinstance(columns.utility_columns.prediction, str):
            preset_tests.append(TestFeatureValueDrift(column_name=columns.utility_columns.prediction))

        preset_tests.append(TestShareOfDriftedFeatures(lt=data.current_data.shape[1] // 3))
        preset_tests.append(TestColumnsType())
        preset_tests.append(TestAllColumnsShareOfNulls())
        preset_tests.append(TestNumColumnsOutOfRangeValues())
        preset_tests.append(TestCatColumnsOutOfListValues())
        preset_tests.append(TestNumColumnsMeanInNSigmas())

        if self.most_important_features:
            preset_tests.append(TestCustomFeaturesValueDrift(features=self.most_important_features))

        return preset_tests
