from numbers import Number
from typing import Optional

from evidently.v2.metrics import DataQualityMetrics
from evidently.v2.metrics import DataStabilityMetrics
from evidently.v2.tests.base_test import Test
from evidently.v2.tests.base_test import TestResult


class TestConflictTarget(Test):
    data_stability_metrics: DataStabilityMetrics

    def __init__(self,
                 data_stability_metrics: Optional[DataStabilityMetrics] = None):
        self.data_stability_metrics = data_stability_metrics if data_stability_metrics is not None \
            else DataStabilityMetrics()

    def check(self):
        conflict_target = self.data_stability_metrics.get_result().target_not_stable
        if conflict_target is None:
            test_result = "ERROR"

        elif conflict_target == 0:
            test_result = "SUCCESS"

        else:
            test_result = "FAIL"

        return TestResult(
            "Test number of conflicts in target",
            f"Number of conflict target values: {conflict_target}",
            test_result
        )


class TestConflictPrediction(Test):
    data_stability_metrics: DataStabilityMetrics

    def __init__(self,
                 data_stability_metrics: Optional[DataStabilityMetrics] = None):
        self.data_stability_metrics = data_stability_metrics if data_stability_metrics is not None \
            else DataStabilityMetrics()

    def check(self):
        conflict_prediction = self.data_stability_metrics.get_result().target_not_stable

        if conflict_prediction is None:
            test_result = "ERROR"

        elif conflict_prediction == 0:
            test_result = "SUCCESS"

        else:
            test_result = "FAIL"

        return TestResult(
            "Test number of conflicts in prediction",
            f"Number of conflict prediction values: {conflict_prediction}",
            test_result
        )


class TestValueMin(Test):
    data_quality_metrics: DataQualityMetrics
    feature_name: str
    gte: Number

    def __init__(self, feature_name: str, gte: Number, data_quality_metrics: Optional[DataQualityMetrics] = None):
        self.data_quality_metrics = data_quality_metrics if data_quality_metrics is not None else DataQualityMetrics()
        self.feature_name = feature_name
        self.gte = gte

    def check(self):
        features_stats = self.data_quality_metrics.get_result().features_stats.get_all_features()
        
        if self.feature_name in features_stats:
            min_value = features_stats[self.feature_name].min
            details = f"Min value for feature '{self.feature_name}' is {min_value}"
    
            if min_value is None:
                test_result = "ERROR"
                details = f"No min value for a feature '{self.feature_name}'"

            elif not isinstance(min_value, Number):
                test_result = "ERROR"
                details = f"Feature '{self.feature_name}' is not numeric"
    
            elif min_value >= self.gte:
                test_result = "SUCCESS"
    
            else:
                test_result = "FAIL"
        
        else:
            test_result = "ERROR"
            details = f"Feature '{self.feature_name}' was not found"

        return TestResult(
            "Test min value of a feature",
            details,
            test_result
        )
