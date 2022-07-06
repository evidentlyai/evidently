from typing import List, Optional

from evidently.analyzers.utils import DatasetColumns
from evidently.v2.metrics.base_metric import InputData
from evidently.v2.test_preset.test_preset import TestPreset
from evidently.v2.tests import (
    TestFeatureValueDrift,
    TestShareOfDriftedFeatures,
    TestColumnNANShare,
    TestShareOfOutRangeValues,
    TestShareOfOutListValues,
    TestMeanInNSigmas,
    TestColumnsType,
)


class NoTargetPerformance(TestPreset):
    def __init__(self, most_important_features: Optional[List[str]] = None):
        super().__init__()
        self.most_important_features = [] if most_important_features is None else most_important_features

    def generate_tests(self, data: InputData, columns: DatasetColumns):
        all_columns = [
            name
            for name in columns.cat_feature_names
            + columns.num_feature_names
            + [
                columns.utility_columns.id_column,
                columns.utility_columns.date,
                columns.utility_columns.target,
                columns.utility_columns.prediction,
            ]
            if name is not None
        ]
        return [
            TestFeatureValueDrift(column_name=columns.utility_columns.prediction),
            TestShareOfDriftedFeatures(lt=data.current_data.shape[1] // 3),
            TestColumnsType(),
            *[TestColumnNANShare(column_name=name) for name in all_columns],
            *[TestShareOfOutRangeValues(column_name=name) for name in columns.num_feature_names],
            *[TestShareOfOutListValues(column_name=name) for name in columns.cat_feature_names],
            *[TestMeanInNSigmas(column_name=name, n_sigmas=2) for name in columns.num_feature_names],
            *[TestFeatureValueDrift(column_name=name) for name in self.most_important_features],
        ]
