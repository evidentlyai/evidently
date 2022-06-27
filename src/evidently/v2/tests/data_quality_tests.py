from numbers import Number
from typing import List
from typing import Optional
from typing import Union

from evidently.v2.metrics import DataQualityMetrics
from evidently.v2.tests.base_test import BaseCheckValueTest
from evidently.v2.tests.base_test import TestResult


class BaseDataQualityMetricsValueTest(BaseCheckValueTest):
    metric: DataQualityMetrics

    def __init__(
        self,
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

        super().__init__(eq=eq, gt=gt, gte=gte, is_in=is_in, lt=lt, lte=lte, not_eq=not_eq, not_in=not_in)


class TestConflictTarget(BaseDataQualityMetricsValueTest):
    name = "Test number of conflicts in target"

    def calculate_value_for_test(self) -> Number:
        return self.metric.get_result().target_not_stable

    def get_description(self, value: Number) -> str:
        return f"Number of conflict target value is {value}"


class TestConflictPrediction(BaseDataQualityMetricsValueTest):
    name = "Test number of conflicts in prediction"

    def calculate_value_for_test(self) -> Number:
        return self.metric.get_result().prediction_not_stable

    def get_description(self, value: Number) -> str:
        return f"Number of conflict prediction value is {value}"


class TestTargetPredictionCorrelation(BaseDataQualityMetricsValueTest):
    name = "Test correlation between target and prediction"

    def calculate_value_for_test(self) -> Number:
        return self.metric.get_result().target_prediction_correlation

    def get_description(self, value: Number) -> str:
        return f"Correlation between target and prediction is {value}"


class BaseFeatureDataQualityMetricsTest(BaseDataQualityMetricsValueTest):
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
        self.feature_name = feature_name
        super().__init__(
            eq=eq, gt=gt, gte=gte, is_in=is_in, lt=lt, lte=lte, not_eq=not_eq, not_in=not_in, metric=metric
        )

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


class TestFeatureValueMax(BaseFeatureDataQualityMetricsTest):
    name = "Test a feature max value"

    def calculate_value_for_test(self) -> Number:
        features_stats = self.metric.get_result().features_stats.get_all_features()
        return features_stats[self.feature_name].max

    def get_description(self, value: Number) -> str:
        return f"Max value for feature '{self.feature_name}' is {value}"


class TestFeatureValueMean(BaseFeatureDataQualityMetricsTest):
    name = "Test a feature mean value"

    def calculate_value_for_test(self) -> Number:
        features_stats = self.metric.get_result().features_stats.get_all_features()
        return features_stats[self.feature_name].mean

    def get_description(self, value: Number) -> str:
        return f"Mean value for feature '{self.feature_name}' is {value}"
