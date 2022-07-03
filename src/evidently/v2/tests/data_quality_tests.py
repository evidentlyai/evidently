from abc import ABC
from numbers import Number
from typing import List
from typing import Optional
from typing import Union

import numpy as np

from evidently.model.widget import BaseWidgetInfo
from evidently.v2.metrics import DataQualityMetrics
from evidently.v2.metrics import DataQualityStabilityMetrics
from evidently.v2.metrics import DataQualityValueListMetrics
from evidently.v2.metrics import DataQualityValueRangeMetrics
from evidently.v2.metrics import DataQualityValueQuantileMetrics
from evidently.v2.renderers.base_renderer import default_renderer, TestRenderer, TestHtmlInfo, DetailsInfo
from evidently.v2.tests.base_test import BaseCheckValueTest
from evidently.v2.tests.base_test import TestValueCondition
from evidently.v2.tests.base_test import Test
from evidently.v2.tests.base_test import TestResult
from evidently.v2.tests.utils import plot_check, plot_metric_value, plot_distr, plot_value_counts_tables, plot_value_counts_tables_ref_curr


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


class TestConflictTarget(Test):
    name = "Test number of conflicts in target"
    metric: DataQualityStabilityMetrics

    def __init__(
        self,
        metric: Optional[DataQualityStabilityMetrics] = None
    ):
        if metric is not None:
            self.metric = metric

        else:
            self.metric = DataQualityStabilityMetrics()

    def check(self):
        metric_result = self.metric.get_result()

        if metric_result.number_not_stable_target is None:
            test_result = TestResult.ERROR
            description = "No target in the dataset"

        elif metric_result.number_not_stable_target > 0:
            test_result = TestResult.FAIL
            description = f"Not stable target rows count is {metric_result.number_not_stable_target}"

        else:
            test_result = TestResult.SUCCESS
            description = "Target is stable"

        return TestResult(name=self.name, description=description, status=test_result)


class TestConflictPrediction(Test):
    name = "Test number of conflicts in prediction"
    metric: DataQualityStabilityMetrics

    def __init__(
            self,
            metric: Optional[DataQualityStabilityMetrics] = None
    ):
        if metric is not None:
            self.metric = metric

        else:
            self.metric = DataQualityStabilityMetrics()

    def check(self):
        metric_result = self.metric.get_result()

        if metric_result.number_not_stable_prediction is None:
            test_result = TestResult.ERROR
            description = "No prediction in the dataset"

        elif metric_result.number_not_stable_prediction > 0:
            test_result = TestResult.FAIL
            description = f"Not stable prediction rows count is {metric_result.number_not_stable_prediction}"

        else:
            test_result = TestResult.SUCCESS
            description = "Prediction is stable"

        return TestResult(name=self.name, description=description, status=test_result)


class TestTargetPredictionCorrelation(BaseDataQualityMetricsValueTest):
    name = "Test correlation between target and prediction"

    def calculate_value_for_test(self) -> Number:
        return self.metric.get_result().target_prediction_correlation

    def get_description(self, value: Number) -> str:
        return f"Correlation between target and prediction is {value}"


class BaseFeatureDataQualityMetricsTest(BaseDataQualityMetricsValueTest, ABC):
    column_name: Union[str, List[str]]

    def __init__(
        self,
        column_name: Union[str, List[str]],
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
        self.column_name = column_name
        super().__init__(
            eq=eq, gt=gt, gte=gte, is_in=is_in, lt=lt, lte=lte, not_eq=not_eq, not_in=not_in, metric=metric
        )

    def check(self):
        result = TestResult(name=self.name, description="The test was not launched", status=TestResult.SKIPPED)
        features_stats = self.metric.get_result().features_stats.get_all_features()

        if self.column_name not in features_stats:
            result.mark_as_fail()
            result.description = f"Feature '{self.column_name}' was not found"
            return result

        value = self.calculate_value_for_test()

        if value is None:
            result.mark_as_error(f"No value for the feature '{self.column_name}'")
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
        return features_stats[self.column_name].min

    def get_description(self, value: Number) -> str:
        return f"Min value for feature '{self.column_name}' is {value}"


@default_renderer(test_type=TestFeatureValueMin)
class TestFeatureValueMinRenderer(TestRenderer):
    def render_html(self, obj: TestFeatureValueMin) -> TestHtmlInfo:
        column_name = obj.column_name
        info = super().render_html(obj)
        curr_distr = obj.metric.get_result().distr_for_plots[column_name]['current']
        ref_distr = None
        if 'reference' in obj.metric.get_result().distr_for_plots[column_name].keys():
            ref_distr = obj.metric.get_result().distr_for_plots[column_name]['reference']
        fig = plot_distr(curr_distr, ref_distr)
        fig = plot_check(fig, obj.condition)
        fig = plot_metric_value(fig, obj.metric.get_result().features_stats[column_name].min, 
                                f'current {column_name} min value')

        fig_json = fig.to_plotly_json()
        info.details.append(
            DetailsInfo(
                id=f"min_{column_name}",
                title="",
                info=BaseWidgetInfo(
                    title="",
                    size=2,
                    type="big_graph",
                    params={"data": fig_json['data'], "layout": fig_json['layout']},
                )
            )
        )
        return info


class TestFeatureValueMax(BaseFeatureDataQualityMetricsTest):
    name = "Test a feature max value"

    def calculate_value_for_test(self) -> Number:
        features_stats = self.metric.get_result().features_stats.get_all_features()
        return features_stats[self.column_name].max

    def get_description(self, value: Number) -> str:
        return f"Max value for feature '{self.column_name}' is {value}"


@default_renderer(test_type=TestFeatureValueMax)
class TestFeatureValueMaxRenderer(TestRenderer):
    def render_html(self, obj: TestFeatureValueMax) -> TestHtmlInfo:
        column_name = obj.column_name
        info = super().render_html(obj)
        curr_distr = obj.metric.get_result().distr_for_plots[column_name]['current']
        ref_distr = None
        if 'reference' in obj.metric.get_result().distr_for_plots[column_name].keys():
            ref_distr = obj.metric.get_result().distr_for_plots[column_name]['reference']
        fig = plot_distr(curr_distr, ref_distr)
        fig = plot_check(fig, obj.condition)
        fig = plot_metric_value(fig, obj.metric.get_result().features_stats[column_name].max, 
                                f'current {column_name} max value')

        fig_json = fig.to_plotly_json()
        info.details.append(
            DetailsInfo(
                id=f"max_{column_name}",
                title="",
                info=BaseWidgetInfo(
                    title="",
                    size=2,
                    type="big_graph",
                    params={"data": fig_json['data'], "layout": fig_json['layout']},
                )
            )
        )
        return info


class TestFeatureValueMean(BaseFeatureDataQualityMetricsTest):
    name = "Test a feature mean value"

    def calculate_value_for_test(self) -> Number:
        features_stats = self.metric.get_result().features_stats.get_all_features()
        return features_stats[self.column_name].mean

    def get_description(self, value: Number) -> str:
        return f"Mean value for feature '{self.column_name}' is {value}"


@default_renderer(test_type=TestFeatureValueMean)
class TestFeatureValueMeanRenderer(TestRenderer):
    def render_html(self, obj: TestFeatureValueMean) -> TestHtmlInfo:
        column_name = obj.column_name
        info = super().render_html(obj)
        curr_distr = obj.metric.get_result().distr_for_plots[column_name]['current']
        ref_distr = None
        if 'reference' in obj.metric.get_result().distr_for_plots[column_name].keys():
            ref_distr = obj.metric.get_result().distr_for_plots[column_name]['reference']
        fig = plot_distr(curr_distr, ref_distr)
        fig = plot_check(fig, obj.condition)
        fig = plot_metric_value(fig, obj.metric.get_result().features_stats[column_name].mean, 
                                f'current {column_name} mean value')

        fig_json = fig.to_plotly_json()
        info.details.append(
            DetailsInfo(
                id=f"mean_{column_name}",
                title="",
                info=BaseWidgetInfo(
                    title="",
                    size=2,
                    type="big_graph",
                    params={"data": fig_json['data'], "layout": fig_json['layout']},
                )
            )
        )
        return info


class TestFeatureValueMedian(BaseFeatureDataQualityMetricsTest):
    name = "Test a feature median value"

    def calculate_value_for_test(self) -> Number:
        features_stats = self.metric.get_result().features_stats.get_all_features()
        return features_stats[self.column_name].percentile_50

    def get_description(self, value: Number) -> str:
        return f"Median (50 percentile) value for feature '{self.column_name}' is {value}"


@default_renderer(test_type=TestFeatureValueMedian)
class TestFeatureValueMedianRenderer(TestRenderer):
    def render_html(self, obj: TestFeatureValueMedian) -> TestHtmlInfo:
        column_name = obj.column_name
        info = super().render_html(obj)
        curr_distr = obj.metric.get_result().distr_for_plots[column_name]['current']
        ref_distr = None
        if 'reference' in obj.metric.get_result().distr_for_plots[column_name].keys():
            ref_distr = obj.metric.get_result().distr_for_plots[column_name]['reference']
        fig = plot_distr(curr_distr, ref_distr)
        fig = plot_check(fig, obj.condition)
        fig = plot_metric_value(fig, obj.metric.get_result().features_stats[column_name].percentile_50, 
                                f'current {column_name} median value')

        fig_json = fig.to_plotly_json()
        info.details.append(
            DetailsInfo(
                id=f"median_{column_name}",
                title="",
                info=BaseWidgetInfo(
                    title="",
                    size=2,
                    type="big_graph",
                    params={"data": fig_json['data'], "layout": fig_json['layout']},
                )
            )
        )
        return info


class TestFeatureValueStd(BaseFeatureDataQualityMetricsTest):
    name = "Test a feature std value"

    def calculate_value_for_test(self) -> Number:
        features_stats = self.metric.get_result().features_stats.get_all_features()
        return features_stats[self.column_name].std

    def get_description(self, value: Number) -> str:
        return f"Std value for feature '{self.column_name}' is {value}"


@default_renderer(test_type=TestFeatureValueStd)
class TestFeatureValueStdRenderer(TestRenderer):
    def render_html(self, obj: TestFeatureValueStd) -> TestHtmlInfo:
        column_name = obj.column_name
        info = super().render_html(obj)
        curr_distr = obj.metric.get_result().distr_for_plots[column_name]['current']
        ref_distr = None
        if 'reference' in obj.metric.get_result().distr_for_plots[column_name].keys():
            ref_distr = obj.metric.get_result().distr_for_plots[column_name]['reference']
        fig = plot_distr(curr_distr, ref_distr)

        fig_json = fig.to_plotly_json()
        info.details.append(
            DetailsInfo(
                id=f"std_{column_name}",
                title="",
                info=BaseWidgetInfo(
                    title="",
                    size=2,
                    type="big_graph",
                    params={"data": fig_json['data'], "layout": fig_json['layout']},
                )
            )
        )
        return info


class TestNumberOfUniqueValues(BaseFeatureDataQualityMetricsTest):
    name = "Test a feature for number of unique values"

    def calculate_value_for_test(self) -> Number:
        features_stats = self.metric.get_result().features_stats.get_all_features()
        return features_stats[self.column_name].unique_count

    def get_description(self, value: Number) -> str:
        return f"Number of unique values for feature '{self.column_name}' is {value}"


@default_renderer(test_type=TestNumberOfUniqueValues)
class TestNumberOfUniqueValuesRenderer(TestRenderer):
    def render_html(self, obj: TestNumberOfUniqueValues) -> TestHtmlInfo:
        info = super().render_html(obj)
        column_name = obj.column_name
        curr_df = obj.metric.get_result().counts_of_values[column_name]['current']
        ref_df = None
        if 'reference' in obj.metric.get_result().counts_of_values[column_name].keys():
            ref_df = obj.metric.get_result().counts_of_values[column_name]['reference']
        additional_plots = plot_value_counts_tables_ref_curr(column_name, curr_df, ref_df, 'num_of_unique_vals')
        info.details = additional_plots
        return info

class TestUniqueValuesShare(BaseFeatureDataQualityMetricsTest):
    name = "Test a feature for share of unique values"

    def calculate_value_for_test(self) -> Number:
        features_stats = self.metric.get_result().features_stats.get_all_features()
        return features_stats[self.column_name].unique_percentage / 100.

    def get_description(self, value: Number) -> str:
        return f"Share of unique values for feature '{self.column_name}' is {value}"


@default_renderer(test_type=TestUniqueValuesShare)
class TestUniqueValuesShareRenderer(TestRenderer):
    def render_html(self, obj: TestUniqueValuesShare) -> TestHtmlInfo:
        info = super().render_html(obj)
        column_name = obj.column_name
        curr_df = obj.metric.get_result().counts_of_values[column_name]['current']
        ref_df = None
        if 'reference' in obj.metric.get_result().counts_of_values[column_name].keys():
            ref_df = obj.metric.get_result().counts_of_values[column_name]['reference']
        additional_plots = plot_value_counts_tables_ref_curr(column_name, curr_df, ref_df, 'unique_vals_sare')
        info.details = additional_plots
        return info


class TestMostCommonValueShare(BaseFeatureDataQualityMetricsTest):
    name = "Test a feature for share of most common value"

    def calculate_value_for_test(self) -> Number:
        features_stats = self.metric.get_result().features_stats.get_all_features()
        return features_stats[self.column_name].most_common_value_percentage / 100.

    def get_description(self, value: Number) -> str:
        return f"Share of most common value for feature '{self.column_name}' is {value}"


@default_renderer(test_type=TestMostCommonValueShare)
class TestMostCommonValueShareRenderer(TestRenderer):
    def render_html(self, obj: TestMostCommonValueShare) -> TestHtmlInfo:
        info = super().render_html(obj)
        column_name = obj.column_name
        curr_df = obj.metric.get_result().counts_of_values[column_name]['current']
        ref_df = None
        if 'reference' in obj.metric.get_result().counts_of_values[column_name].keys():
            ref_df = obj.metric.get_result().counts_of_values[column_name]['reference']
        additional_plots = plot_value_counts_tables_ref_curr(column_name, curr_df, ref_df, 'most_common_value_sare')
        info.details = additional_plots
        return info


class TestMeanInNSigmas(Test):
    name = "Test mean value in N sigmas by reference"
    metric: DataQualityMetrics
    column_name: str
    n_sigmas: int

    def __init__(
            self,
            column_name: str,
            n_sigmas: int = 2,
            metric: Optional[DataQualityMetrics] = None
    ):
        self.column_name = column_name
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

        if self.column_name not in features_stats.get_all_features():
            description = f"Column {self.column_name} should be in current data"
            test_result = TestResult.ERROR

        elif self.column_name not in reference_feature_stats.get_all_features():
            description = f"Column {self.column_name} should be in reference data"
            test_result = TestResult.ERROR

        else:
            current_mean = features_stats[self.column_name].mean
            reference_mean = reference_feature_stats[self.column_name].mean
            reference_std = reference_feature_stats[self.column_name].std
            sigmas_value = reference_std * self.n_sigmas
            left_condition = reference_mean - sigmas_value
            right_condition = reference_mean + sigmas_value

            if left_condition < current_mean < right_condition:
                description = f"Mean {np.round(current_mean, 3)} is in range from {np.round(left_condition, 3)} \
                                to {np.round(right_condition, 3)}"
                test_result = TestResult.SUCCESS

            else:
                description = f"Mean {np.round(current_mean, 3)} is not in range from {np.round(left_condition, 3)} \
                                to {np.round(right_condition, 3)}"
                test_result = TestResult.FAIL

        return TestResult(name=self.name, description=description, status=test_result)


@default_renderer(test_type=TestMeanInNSigmas)
class TestMeanInNSigmasRenderer(TestRenderer):
    def render_html(self, obj: TestMeanInNSigmas) -> TestHtmlInfo:
        column_name = obj.column_name
        ref_mean = obj.metric.get_result().reference_features_stats[column_name].mean
        ref_std = obj.metric.get_result().reference_features_stats[column_name].std
        gt = ref_mean - obj.n_sigmas * ref_std
        lt = ref_mean + obj.n_sigmas * ref_std
        ref_condition = TestValueCondition(gt=gt, lt=lt)
        info = super().render_html(obj)
        curr_distr = obj.metric.get_result().distr_for_plots[column_name]['current']
        ref_distr = None
        if 'reference' in obj.metric.get_result().distr_for_plots[column_name].keys():
            ref_distr = obj.metric.get_result().distr_for_plots[column_name]['reference']
        fig = plot_distr(curr_distr, ref_distr)
        fig = plot_check(fig, ref_condition)
        fig = plot_metric_value(fig, obj.metric.get_result().features_stats[column_name].mean, 
                                f'current {column_name} mean value')

        fig_json = fig.to_plotly_json()
        info.details.append(
            DetailsInfo(
                id=f"mean_in_n_sigmas_{column_name}",
                title="",
                info=BaseWidgetInfo(
                    title="",
                    size=2,
                    type="big_graph",
                    params={"data": fig_json['data'], "layout": fig_json['layout']},
                )
            )
        )
        return info


class TestValueRange(Test):
    name = "Checks that all values of certain column belong to the interval"
    metric: DataQualityValueRangeMetrics
    column: str
    left: Optional[float]
    right: Optional[float]

    def __init__(
            self,
            column_name: str,
            left: Optional[float] = None,
            right: Optional[float] = None,
            metric: Optional[DataQualityValueRangeMetrics] = None
    ):
        self.column_name = column_name
        self.left = left
        self.right = right

        if metric is not None:
            self.metric = metric

        else:
            self.metric = DataQualityValueRangeMetrics(column=column_name, left=left, right=right)

    def check(self):
        number_not_in_range = self.metric.get_result().number_not_in_range

        if number_not_in_range > 0:
            description = f"Column {self.column_name} has {number_not_in_range} values that are " \
                          f"not in range from {self.left} to {self.right}."
            test_result = TestResult.FAIL
        else:
            description = f"Column {self.column_name} values are in range from {self.left} to {self.right}"
            test_result = TestResult.SUCCESS

        return TestResult(name=self.name, description=description, status=test_result)


@default_renderer(test_type=TestValueRange)
class TestValueRangeRenderer(TestRenderer):
    def render_html(self, obj: TestValueRange) -> TestHtmlInfo:
        column_name = obj.column_name
        condition_ = TestValueCondition(gt=obj.left, lt=obj.right)
        info = super().render_html(obj)
        curr_distr = obj.metric.get_result().distr_for_plot['current']
        ref_distr = None
        if 'reference' in obj.metric.get_result().distr_for_plot.keys():
            ref_distr = obj.metric.get_result().distr_for_plot['reference']
        fig = plot_distr(curr_distr, ref_distr)
        fig = plot_check(fig, condition_)

        fig_json = fig.to_plotly_json()
        info.details.append(
            DetailsInfo(
                id=f"value_range_{column_name}",
                title="",
                info=BaseWidgetInfo(
                    title="",
                    size=2,
                    type="big_graph",
                    params={"data": fig_json['data'], "layout": fig_json['layout']},
                )
            )
        )
        return info


class BaseDataQualityValueRangeMetricsTest(BaseCheckValueTest, ABC):
    metric: DataQualityValueRangeMetrics
    column: str
    left: Optional[float]
    right: Optional[float]

    def __init__(
        self,
        column_name: str,
        left: Optional[float] = None,
        right: Optional[float] = None,
        eq: Optional[Number] = None,
        gt: Optional[Number] = None,
        gte: Optional[Number] = None,
        is_in: Optional[List[Union[Number, str, bool]]] = None,
        lt: Optional[Number] = None,
        lte: Optional[Number] = None,
        not_eq: Optional[Number] = None,
        not_in: Optional[List[Union[Number, str, bool]]] = None,
        metric: Optional[DataQualityValueRangeMetrics] = None
    ):
        self.column_name = column_name
        self.left = left
        self.right = right

        if metric is not None:
            self.metric = metric

        else:
            self.metric = DataQualityValueRangeMetrics(column=column_name, left=left, right=right)

        super().__init__(eq=eq, gt=gt, gte=gte, is_in=is_in, lt=lt, lte=lte, not_eq=not_eq, not_in=not_in)


class TestNumberOfOutRangeValues(BaseDataQualityValueRangeMetricsTest):
    name = "Test the number of out range values for a given feature and compares it against the threshold"

    def calculate_value_for_test(self) -> Number:
        return self.metric.get_result().number_not_in_range

    def get_description(self, value: Number) -> str:
        return f"Number of out of the range values for feature '{self.column_name}' is {value}"


@default_renderer(test_type=TestNumberOfOutRangeValues)
class TestNumberOfOutRangeValuesRenderer(TestRenderer):
    def render_html(self, obj: TestNumberOfOutRangeValues) -> TestHtmlInfo:
        column_name = obj.column_name
        condition_ = TestValueCondition(gt=obj.left, lt=obj.right)
        info = super().render_html(obj)
        curr_distr = obj.metric.get_result().distr_for_plot['current']
        ref_distr = None
        if 'reference' in obj.metric.get_result().distr_for_plot.keys():
            ref_distr = obj.metric.get_result().distr_for_plot['reference']
        fig = plot_distr(curr_distr, ref_distr)
        fig = plot_check(fig, condition_)

        fig_json = fig.to_plotly_json()
        info.details.append(
            DetailsInfo(
                id=f"num_out_of_range_{column_name}",
                title="",
                info=BaseWidgetInfo(
                    title="",
                    size=2,
                    type="big_graph",
                    params={"data": fig_json['data'], "layout": fig_json['layout']},
                )
            )
        )
        return info


class TestShareOfOutRangeValues(BaseDataQualityValueRangeMetricsTest):
    name = "Test the share of out of the range values for a given feature and compares it against the threshold"

    def calculate_value_for_test(self) -> Number:
        return self.metric.get_result().share_not_in_range

    def get_description(self, value: Number) -> str:
        return f"Share of out of the range values for feature '{self.column_name}' is {value}"


@default_renderer(test_type=TestShareOfOutRangeValues)
class TestShareOfOutRangeValuesRenderer(TestRenderer):
    def render_html(self, obj: TestShareOfOutRangeValues) -> TestHtmlInfo:
        column_name = obj.column_name
        condition_ = TestValueCondition(gt=obj.left, lt=obj.right)
        info = super().render_html(obj)
        curr_distr = obj.metric.get_result().distr_for_plot['current']
        ref_distr = None
        if 'reference' in obj.metric.get_result().distr_for_plot.keys():
            ref_distr = obj.metric.get_result().distr_for_plot['reference']
        fig = plot_distr(curr_distr, ref_distr)
        fig = plot_check(fig, condition_)

        fig_json = fig.to_plotly_json()
        info.details.append(
            DetailsInfo(
                id=f"share_out_of_range_{column_name}",
                title="",
                info=BaseWidgetInfo(
                    title="",
                    size=2,
                    type="big_graph",
                    params={"data": fig_json['data'], "layout": fig_json['layout']},
                )
            )
        )
        return info


class TestValueList(Test):
    name = "Test checks whether a feature values is in some list of values"
    metric: DataQualityValueListMetrics
    column_name: str
    values: Optional[list]

    def __init__(
        self,
        column_name: str,
        values: Optional[list] = None,
        metric: Optional[DataQualityValueListMetrics] = None
    ):
        self.column_name = column_name
        self.values = values

        if metric is not None:
            self.metric = metric

        else:
            self.metric = DataQualityValueListMetrics(column=column_name, values=values)

    def check(self):
        metric_result = self.metric.get_result()

        if metric_result.number_not_in_list > 0:
            test_result = TestResult.FAIL
            description = f"Number values not in the values list is {metric_result.number_not_in_list}"

        else:
            test_result = TestResult.SUCCESS
            description = "All values is in the values list"

        return TestResult(name=self.name, description=description, status=test_result)


@default_renderer(test_type=TestValueList)
class TestValueListRenderer(TestRenderer):
    def render_html(self, obj: TestValueList) -> TestHtmlInfo:
        info = super().render_html(obj)
        column_name = obj.column_name
        values = obj.values
        curr_df = obj.metric.get_result().counts_of_value['current']
        ref_df = None
        if 'reference' in obj.metric.get_result().counts_of_value.keys():
            ref_df = obj.metric.get_result().counts_of_value['reference']
        additional_plots = plot_value_counts_tables(column_name, values, curr_df, ref_df, 'value_list')
        info.details = additional_plots
        return info


class BaseDataQualityValueListMetricsTest(BaseCheckValueTest, ABC):
    metric: DataQualityValueListMetrics
    column: str
    values: Optional[list]

    def __init__(
        self,
        column_name: str,
        values: Optional[list] = None,
        eq: Optional[Number] = None,
        gt: Optional[Number] = None,
        gte: Optional[Number] = None,
        is_in: Optional[List[Union[Number, str, bool]]] = None,
        lt: Optional[Number] = None,
        lte: Optional[Number] = None,
        not_eq: Optional[Number] = None,
        not_in: Optional[List[Union[Number, str, bool]]] = None,
        metric: Optional[DataQualityValueListMetrics] = None
    ):
        self.column_name = column_name
        self.values = values

        if metric is not None:
            self.metric = metric

        else:
            self.metric = DataQualityValueListMetrics(column=column_name, values=values)

        super().__init__(eq=eq, gt=gt, gte=gte, is_in=is_in, lt=lt, lte=lte, not_eq=not_eq, not_in=not_in)


class TestNumberOfOutListValues(BaseDataQualityValueListMetricsTest):
    name = "Test the number of out list values for a given feature and compares it against the threshold"

    def calculate_value_for_test(self) -> Number:
        return self.metric.get_result().number_not_in_list

    def get_description(self, value: Number) -> str:
        return f"Number of out of the list values for feature '{self.column_name}' is {value}"


@default_renderer(test_type=TestNumberOfOutListValues)
class TestNumberOfOutListValuesRenderer(TestRenderer):
    def render_html(self, obj: TestNumberOfOutListValues) -> TestHtmlInfo:
        info = super().render_html(obj)
        column_name = obj.column_name
        values = obj.values
        curr_df = obj.metric.get_result().counts_of_value['current']
        ref_df = None
        if 'reference' in obj.metric.get_result().counts_of_value.keys():
            ref_df = obj.metric.get_result().counts_of_value['reference']
        additional_plots = plot_value_counts_tables(column_name, values, curr_df, ref_df, 'number_value_list')
        info.details = additional_plots
        return info


class TestShareOfOutListValues(BaseDataQualityValueListMetricsTest):
    name = "Test the share of out list values for a given feature and compares it against the threshold"

    def calculate_value_for_test(self) -> Number:
        return self.metric.get_result().share_not_in_list

    def get_description(self, value: Number) -> str:
        return f"Share of out of the list values for feature '{self.column_name}' is {value}"


class TestValueQuantile(BaseCheckValueTest):
    name = "Test calculates quantile value of a given column and compares it against the threshold"
    metric: DataQualityValueQuantileMetrics
    column: str
    quantile: Optional[float]

    def __init__(
        self,
        column: str,
        quantile: Optional[float],
        eq: Optional[Number] = None,
        gt: Optional[Number] = None,
        gte: Optional[Number] = None,
        is_in: Optional[List[Union[Number, str, bool]]] = None,
        lt: Optional[Number] = None,
        lte: Optional[Number] = None,
        not_eq: Optional[Number] = None,
        not_in: Optional[List[Union[Number, str, bool]]] = None,
        metric: Optional[DataQualityValueQuantileMetrics] = None
    ):
        self.column = column
        self.quantile = quantile

        if metric is not None:
            if column is not None or quantile is not None:
                raise ValueError("Test parameters and given  metric conflict")

            self.metric = metric

        else:
            self.metric = DataQualityValueQuantileMetrics(column=column, quantile=quantile)

        super().__init__(eq=eq, gt=gt, gte=gte, is_in=is_in, lt=lt, lte=lte, not_eq=not_eq, not_in=not_in)

    def calculate_value_for_test(self) -> Number:
        return self.metric.get_result().value

    def get_description(self, value: Number) -> str:
        return f"Quantile {self.quantile} for column '{self.column}' is {value}"


@default_renderer(test_type=TestShareOfOutListValues)
class TestShareOfOutListValuesRenderer(TestRenderer):
    def render_html(self, obj: TestShareOfOutListValues) -> TestHtmlInfo:
        info = super().render_html(obj)
        column_name = obj.column_name
        values = obj.values
        curr_df = obj.metric.get_result().counts_of_value['current']
        ref_df = None
        if 'reference' in obj.metric.get_result().counts_of_value.keys():
            ref_df = obj.metric.get_result().counts_of_value['reference']
        additional_plots = plot_value_counts_tables(column_name, values, curr_df, ref_df, 'share_value_list')
        info.details = additional_plots
        return info
