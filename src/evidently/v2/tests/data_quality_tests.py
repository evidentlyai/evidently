from numbers import Number
from typing import List
from typing import Optional
from typing import Union

from evidently.v2.metrics import DataQualityMetrics
from evidently.v2.metrics import DataStabilityMetrics
from evidently.v2.tests.base_test import BaseValueTest
from evidently.v2.tests.base_test import Test
from evidently.v2.tests.base_test import TestResult


class TestConflictTarget(Test):
    data_stability_metrics: DataStabilityMetrics

    def __init__(self, data_stability_metrics: Optional[DataStabilityMetrics] = None):
        if data_stability_metrics is not None:
            self.data_stability_metrics = data_stability_metrics

        else:
            self.data_stability_metrics = DataStabilityMetrics()

    def check(self):
        conflict_target = self.data_stability_metrics.get_result().target_not_stable
        if conflict_target is None:
            test_result = TestResult.ERROR

        elif conflict_target == 0:
            test_result = TestResult.SUCCESS

        else:
            test_result = TestResult.FAIL

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
            test_result = TestResult.ERROR

        elif conflict_prediction == 0:
            test_result = TestResult.SUCCESS

        else:
            test_result = TestResult.FAIL

        return TestResult(
            "Test number of conflicts in prediction",
            f"Number of conflict prediction values: {conflict_prediction}",
            test_result
        )


class BaseFeatureDataQualityMetricsTest(BaseValueTest):
    metric: DataQualityMetrics
    feature_name: str

    def __init__(
        self,
        feature_name: Union[str, List[str]],
        eq: Optional[Number] = None,
        gt: Optional[Number] = None,
        gte: Optional[Number] = None,
        is_in: Optional[List[Union[Number, str, bool]]] = None,
        lt: Optional[Number] = None,
        lte: Optional[Number] = None,
        not_eq: Optional[Number] = None,
        not_in: Optional[List[Union[Number, str, bool]]] = None,
        metric: Optional[DataQualityMetrics] = None
    ):
        if metric is not None:
            self.metric = metric

        else:
            self.metric = DataQualityMetrics()

        self.feature_name = feature_name
        super().__init__(eq=eq, gt=gt, gte=gte, is_in=is_in, lt=lt, lte=lte, not_eq=not_eq, not_in=not_in)

    def check(self):
        result = TestResult(name=self.name, description="The test was not launched", status=TestResult.SKIPPED)
        features_stats = self.metric.get_result().features_stats.get_all_features()

        if self.feature_name not in features_stats:
            result.mark_as_fail()
            result.description = f"Feature '{self.feature_name}' was not found"
            return result

        value = self.calculate_value_for_test()

        if value is None:
            result.mark_as_error(f"No value for the feature '{self.feature_name}'")
            return result

        result.description = self.get_description(value)

        try:
            condition_check_result = self.condition.check_value(value)

            if condition_check_result:
                result.mark_as_success()

            else:
                result.mark_as_fail()

        except ValueError:
            result.mark_as_error("Cannot calculate the condition")

        return result


class TestFeatureValueMin(BaseFeatureDataQualityMetricsTest):
    name = "Test a feature min value"

    def calculate_value_for_test(self) -> Number:
        features_stats = self.metric.get_result().features_stats.get_all_features()
        return features_stats[self.feature_name].min

    def get_description(self, value: Number) -> str:
        return f"Min value for feature '{self.feature_name}' is {value}"
