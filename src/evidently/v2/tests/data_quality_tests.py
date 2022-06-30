from abc import ABC
from numbers import Number
from typing import List
from typing import Optional
from typing import Union

from evidently.v2.metrics import DataQualityMetrics
from evidently.v2.tests.base_test import BaseCheckValueTest
from evidently.v2.tests.base_test import Test
from evidently.v2.tests.base_test import TestResult


class BaseDataQualityMetricsValueTest(BaseCheckValueTest, ABC):
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


class BaseFeatureDataQualityMetricsTest(BaseDataQualityMetricsValueTest, ABC):
    feature_name: Union[str, List[str]]

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


class TestFeatureValueMedian(BaseFeatureDataQualityMetricsTest):
    name = "Test a feature median value"

    def calculate_value_for_test(self) -> Number:
        features_stats = self.metric.get_result().features_stats.get_all_features()
        return features_stats[self.feature_name].percentile_50

    def get_description(self, value: Number) -> str:
        return f"Median (50 percentile) value for feature '{self.feature_name}' is {value}"


class TestFeatureValueStd(BaseFeatureDataQualityMetricsTest):
    name = "Test a feature std value"

    def calculate_value_for_test(self) -> Number:
        features_stats = self.metric.get_result().features_stats.get_all_features()
        return features_stats[self.feature_name].std

    def get_description(self, value: Number) -> str:
        return f"Std value for feature '{self.feature_name}' is {value}"


class TestNumberOfUniqueValues(BaseFeatureDataQualityMetricsTest):
    name = "Test a feature for number of unique values"

    def calculate_value_for_test(self) -> Number:
        features_stats = self.metric.get_result().features_stats.get_all_features()
        return features_stats[self.feature_name].unique_count

    def get_description(self, value: Number) -> str:
        return f"Number of unique values for feature '{self.feature_name}' is {value}"


class TestUniqueValuesShare(BaseFeatureDataQualityMetricsTest):
    name = "Test a feature for share of unique values"

    def calculate_value_for_test(self) -> Number:
        features_stats = self.metric.get_result().features_stats.get_all_features()
        return features_stats[self.feature_name].unique_percentage / 100.

    def get_description(self, value: Number) -> str:
        return f"Share of unique values for feature '{self.feature_name}' is {value}"


class TestMostCommonValueShare(BaseFeatureDataQualityMetricsTest):
    name = "Test a feature for share of most common value"

    def calculate_value_for_test(self) -> Number:
        features_stats = self.metric.get_result().features_stats.get_all_features()
        return features_stats[self.feature_name].most_common_value_percentage / 100.

    def get_description(self, value: Number) -> str:
        return f"Share of most common value for feature '{self.feature_name}' is {value}"


class TestMeanInNSigmas(Test):
    name = "Test mean value in N sigmas by reference"
    metric: DataQualityMetrics
    column: str
    n_sigmas: int

    def __init__(
            self,
            column: str,
            n_sigmas: int = 2,
            metric: Optional[DataQualityMetrics] = None
    ):
        self.column = column
        self.n_sigmas = n_sigmas
        if metric is not None:
            self.metric = metric

        else:
            self.metric = DataQualityMetrics()

    def check(self):
        reference_feature_stats = self.metric.get_result().reference_features_stats
        features_stats = self.metric.get_result().features_stats

        if not reference_feature_stats:
            raise ValueError("Reference should be present")

        if self.column not in features_stats.get_all_features():
            description = f"Column {self.column} should be in current data"
            test_result = TestResult.ERROR

        elif self.column not in reference_feature_stats.get_all_features():
            description = f"Column {self.column} should be in reference data"
            test_result = TestResult.ERROR

        else:
            current_mean = features_stats[self.column].mean
            reference_mean = reference_feature_stats[self.column].mean
            reference_std = reference_feature_stats[self.column].std
            sigmas_value = reference_std * self.n_sigmas
            left_condition = reference_mean - sigmas_value
            right_condition = reference_mean + sigmas_value

            if left_condition < current_mean < right_condition:
                description = f"Mean {current_mean} is in range from {left_condition} to {right_condition}"
                test_result = TestResult.SUCCESS

            else:
                description = f"Mean {current_mean} is not in range from {left_condition} to {right_condition}"
                test_result = TestResult.FAIL

        return TestResult(name=self.name, description=description, status=test_result)


class TestValueRange(Test):
    name = "Checks that all values of certain column belong to the interval"
    metric: DataQualityMetrics
    column: str
    gt: Optional[int]
    lt: Optional[int]

    def __init__(
            self,
            column: str,
            gt: Optional[int] = None,
            lt: Optional[int] = None,
            metric: Optional[DataQualityMetrics] = None
    ):
        self.column = column
        self.gt = gt
        self.lt = lt

        if metric is not None:
            self.metric = metric

        else:
            self.metric = DataQualityMetrics()

    def check(self):
        reference_feature_stats = self.metric.get_result().reference_features_stats
        features_stats = self.metric.get_result().features_stats

        if (self.gt is None or self.lt is None) and reference_feature_stats is None:
            raise ValueError("Reference should be present")

        if self.column not in features_stats.get_all_features():
            description = f"Column {self.column} should be in current data"
            test_result = TestResult.ERROR

        elif reference_feature_stats and self.column not in reference_feature_stats.get_all_features():
            description = f"Column {self.column} should be in reference data"
            test_result = TestResult.ERROR

        else:
            if self.gt is None:
                min_condition = reference_feature_stats[self.column].min

            else:
                min_condition = self.gt

            if self.lt is None:
                max_condition = reference_feature_stats[self.column].max

            else:
                max_condition = self.lt

            current_min = features_stats[self.column].min
            current_max = features_stats[self.column].max

            if current_min >= min_condition and current_max <= max_condition:
                description = f"Column {self.column} values are in range from {min_condition} to {max_condition}"
                test_result = TestResult.SUCCESS

            else:
                description = f"Column {self.column} values are not in range from {min_condition} to {max_condition}. " \
                              f"Column min value is {current_min}. And max value is {current_max}"
                test_result = TestResult.FAIL

        return TestResult(name=self.name, description=description, status=test_result)