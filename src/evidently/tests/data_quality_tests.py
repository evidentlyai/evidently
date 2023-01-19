from abc import ABC
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import numpy as np
import pandas as pd

from evidently.metrics import ColumnQuantileMetric
from evidently.metrics import ColumnSummaryMetric
from evidently.metrics import ColumnValueListMetric
from evidently.metrics import ColumnValueRangeMetric
from evidently.metrics import ConflictPredictionMetric
from evidently.metrics import ConflictTargetMetric
from evidently.metrics import DatasetCorrelationsMetric
from evidently.metrics.data_integrity.column_summary_metric import NumericCharacteristics
from evidently.renderers.base_renderer import TestHtmlInfo
from evidently.renderers.base_renderer import TestRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import plotly_figure
from evidently.renderers.render_utils import get_distribution_plot_figure
from evidently.renderers.render_utils import plot_distr
from evidently.tests.base_test import BaseCheckValueTest
from evidently.tests.base_test import GroupData
from evidently.tests.base_test import GroupingTypes
from evidently.tests.base_test import Test
from evidently.tests.base_test import TestResult
from evidently.tests.base_test import TestValueCondition
from evidently.tests.utils import approx
from evidently.tests.utils import plot_check
from evidently.tests.utils import plot_correlations
from evidently.tests.utils import plot_metric_value
from evidently.tests.utils import plot_value_counts_tables
from evidently.tests.utils import plot_value_counts_tables_ref_curr
from evidently.utils.data_operations import DatasetColumns
from evidently.utils.generators import BaseGenerator
from evidently.utils.types import Numeric

DATA_QUALITY_GROUP = GroupData("data_quality", "Data Quality", "")
GroupingTypes.TestGroup.add_value(DATA_QUALITY_GROUP)


class BaseDataQualityMetricsValueTest(BaseCheckValueTest, ABC):
    group = DATA_QUALITY_GROUP.id
    metric: ColumnSummaryMetric

    def __init__(
        self,
        column_name: str,
        eq: Optional[Numeric] = None,
        gt: Optional[Numeric] = None,
        gte: Optional[Numeric] = None,
        is_in: Optional[List[Union[Numeric, str, bool]]] = None,
        lt: Optional[Numeric] = None,
        lte: Optional[Numeric] = None,
        not_eq: Optional[Numeric] = None,
        not_in: Optional[List[Union[Numeric, str, bool]]] = None,
    ):
        super().__init__(eq=eq, gt=gt, gte=gte, is_in=is_in, lt=lt, lte=lte, not_eq=not_eq, not_in=not_in)
        self.metric = ColumnSummaryMetric(column_name)


class TestConflictTarget(Test):
    group = DATA_QUALITY_GROUP.id
    name = "Test number of conflicts in target"
    metric: ConflictTargetMetric

    def __init__(self):
        self.metric = ConflictTargetMetric()

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
    group = DATA_QUALITY_GROUP.id
    name = "Test number of conflicts in prediction"
    metric: ConflictPredictionMetric

    def __init__(self):
        self.metric = ConflictPredictionMetric()

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


class BaseDataQualityCorrelationsMetricsValueTest(BaseCheckValueTest, ABC):
    group = DATA_QUALITY_GROUP.id
    metric: DatasetCorrelationsMetric
    method: str

    def __init__(
        self,
        method: str = "pearson",
        eq: Optional[Numeric] = None,
        gt: Optional[Numeric] = None,
        gte: Optional[Numeric] = None,
        is_in: Optional[List[Union[Numeric, str, bool]]] = None,
        lt: Optional[Numeric] = None,
        lte: Optional[Numeric] = None,
        not_eq: Optional[Numeric] = None,
        not_in: Optional[List[Union[Numeric, str, bool]]] = None,
    ):
        self.method = method
        super().__init__(eq=eq, gt=gt, gte=gte, is_in=is_in, lt=lt, lte=lte, not_eq=not_eq, not_in=not_in)
        self.metric = DatasetCorrelationsMetric()


class TestTargetPredictionCorrelation(BaseDataQualityCorrelationsMetricsValueTest):
    name = "Correlation between Target and Prediction"

    def get_condition(self) -> TestValueCondition:
        if self.condition.has_condition():
            return self.condition

        reference = self.metric.get_result().reference

        if reference is not None:
            value = reference.stats[self.method].target_prediction_correlation

            if value is not None:
                return TestValueCondition(eq=approx(value, absolute=0.25))

        return TestValueCondition(gt=0)

    def calculate_value_for_test(self) -> Optional[Numeric]:
        return self.metric.get_result().current.stats[self.method].target_prediction_correlation

    def get_description(self, value: Numeric) -> str:
        if value is None:
            return "No target or prediction in the dataset."
        return (
            f"The correlation between the target and prediction is {value:.3}. "
            f"The test threshold is {self.get_condition()}."
        )


class TestHighlyCorrelatedColumns(BaseDataQualityCorrelationsMetricsValueTest):
    name = "Highly Correlated Columns"

    def get_condition(self) -> TestValueCondition:
        if self.condition.has_condition():
            return self.condition

        reference_correlation = self.metric.get_result().reference

        if reference_correlation is not None:
            value = reference_correlation.stats[self.method].abs_max_features_correlation

            if value is not None:
                return TestValueCondition(eq=approx(value, relative=0.1))

        return TestValueCondition(lt=0.9)

    def calculate_value_for_test(self) -> Optional[Numeric]:
        return self.metric.get_result().current.stats[self.method].abs_max_features_correlation

    def get_description(self, value: Numeric) -> str:
        return f"The maximum correlation is {value:.3g}. The test threshold is {self.get_condition()}."


@default_renderer(wrap_type=TestHighlyCorrelatedColumns)
class TestHighlyCorrelatedColumnsRenderer(TestRenderer):
    def render_json(self, obj: TestHighlyCorrelatedColumns) -> dict:
        base = super().render_json(obj)
        base["parameters"]["condition"] = obj.get_condition().as_dict()
        base["parameters"]["abs_max_num_features_correlation"] = np.round(obj.value, 3)
        return base

    def render_html(self, obj: TestHighlyCorrelatedColumns) -> TestHtmlInfo:
        info = super().render_html(obj)
        metric_result = obj.metric.get_result()
        current_correlations = metric_result.current.correlation[obj.method]

        if metric_result.reference is not None:
            reference_correlations: Optional[pd.DataFrame] = metric_result.reference.correlation[obj.method]

        else:
            reference_correlations = None

        fig = plot_correlations(current_correlations, reference_correlations)
        info.with_details("Highly Correlated Features", plotly_figure(title="", figure=fig))
        return info


class TestTargetFeaturesCorrelations(BaseDataQualityCorrelationsMetricsValueTest):
    name = "Correlation between Target and Features"

    def get_condition(self) -> TestValueCondition:
        if self.condition.has_condition():
            return self.condition

        reference_correlation = self.metric.get_result().reference

        if reference_correlation is not None:
            value = reference_correlation.stats[self.method].abs_max_target_features_correlation

            if value is not None:
                return TestValueCondition(eq=approx(value, relative=0.1))

        return TestValueCondition(lt=0.9)

    def calculate_value_for_test(self) -> Optional[Numeric]:
        return self.metric.get_result().current.stats[self.method].abs_max_target_features_correlation

    def get_description(self, value: Numeric) -> str:
        if value is None:
            return "No target in the current dataset"

        else:
            return f"The maximum correlation is {value:.3g}. The test threshold is {self.get_condition()}."


@default_renderer(wrap_type=TestTargetFeaturesCorrelations)
class TestTargetFeaturesCorrelationsRenderer(TestRenderer):
    def render_json(self, obj: TestTargetFeaturesCorrelations) -> dict:
        base = super().render_json(obj)
        base["parameters"]["condition"] = obj.get_condition().as_dict()

        if obj.value is not None:
            abs_max_target_features_correlation = np.round(obj.value, 3)

        else:
            abs_max_target_features_correlation = obj.value

        base["parameters"]["abs_max_target_features_correlation"] = abs_max_target_features_correlation
        return base

    def render_html(self, obj: TestTargetFeaturesCorrelations) -> TestHtmlInfo:
        info = super().render_html(obj)
        metric_result = obj.metric.get_result()
        current_correlations = metric_result.current.correlation[obj.method]

        if metric_result.reference is not None:
            reference_correlations: Optional[pd.DataFrame] = metric_result.reference.correlation[obj.method]

        else:
            reference_correlations = None

        fig = plot_correlations(current_correlations, reference_correlations)
        info.with_details("Target Features Correlations", plotly_figure(title="", figure=fig))
        return info


class TestPredictionFeaturesCorrelations(BaseDataQualityCorrelationsMetricsValueTest):
    name = "Correlation between Prediction and Features"

    def get_condition(self) -> TestValueCondition:
        if self.condition.has_condition():
            return self.condition

        reference_correlation = self.metric.get_result().reference

        if reference_correlation is not None:
            value = reference_correlation.stats[self.method].abs_max_prediction_features_correlation

            if value is not None:
                return TestValueCondition(eq=approx(value, relative=0.1))

        return TestValueCondition(lt=0.9)

    def calculate_value_for_test(self) -> Optional[Numeric]:
        return self.metric.get_result().current.stats[self.method].abs_max_prediction_features_correlation

    def get_description(self, value: Numeric) -> str:
        if value is None:
            return "No prediction in the current dataset"

        else:
            return f"The maximum correlation is {value:.3g}. The test threshold is {self.get_condition()}."


@default_renderer(wrap_type=TestPredictionFeaturesCorrelations)
class TestPredictionFeaturesCorrelationsRenderer(TestRenderer):
    def render_json(self, obj: TestPredictionFeaturesCorrelations) -> dict:
        base = super().render_json(obj)
        base["parameters"]["condition"] = obj.get_condition().as_dict()

        if obj.value is not None:
            abs_max_prediction_features_correlation = np.round(obj.value, 3)

        else:
            abs_max_prediction_features_correlation = obj.value

        base["parameters"]["abs_max_prediction_features_correlation"] = abs_max_prediction_features_correlation
        return base

    def render_html(self, obj: TestTargetFeaturesCorrelations) -> TestHtmlInfo:
        info = super().render_html(obj)
        metric_result = obj.metric.get_result()
        current_correlations = metric_result.current.correlation[obj.method]

        if metric_result.reference is not None:
            reference_correlations: Optional[pd.DataFrame] = metric_result.reference.correlation[obj.method]

        else:
            reference_correlations = None

        fig = plot_correlations(current_correlations, reference_correlations)
        info.with_details("Target-Features Correlations", plotly_figure(title="", figure=fig))
        return info


class TestCorrelationChanges(BaseDataQualityCorrelationsMetricsValueTest):
    group = DATA_QUALITY_GROUP.id
    name = "Change in Correlation"
    metric: DatasetCorrelationsMetric
    corr_diff: float

    def __init__(
        self,
        corr_diff: float = 0.25,
        method: str = "pearson",
        eq: Optional[Numeric] = None,
        gt: Optional[Numeric] = None,
        gte: Optional[Numeric] = None,
        is_in: Optional[List[Union[Numeric, str, bool]]] = None,
        lt: Optional[Numeric] = None,
        lte: Optional[Numeric] = None,
        not_eq: Optional[Numeric] = None,
        not_in: Optional[List[Union[Numeric, str, bool]]] = None,
    ):
        super().__init__(
            method=method,
            eq=eq,
            gt=gt,
            gte=gte,
            is_in=is_in,
            lt=lt,
            lte=lte,
            not_eq=not_eq,
            not_in=not_in,
        )
        self.corr_diff = corr_diff

    def get_condition(self) -> TestValueCondition:
        if self.condition.has_condition():
            return self.condition

        return TestValueCondition(eq=0)

    def calculate_value_for_test(self) -> Optional[Numeric]:
        metric_result = self.metric.get_result()

        if metric_result.reference is None:
            raise ValueError("Reference should be present")

        current_correlations = metric_result.current.correlation[self.method]
        reference_correlations: Optional[pd.DataFrame] = metric_result.reference.correlation[self.method]
        diff = reference_correlations - current_correlations
        return (diff.abs() > self.corr_diff).sum().sum() / 2

    def get_description(self, value: Numeric) -> str:
        return f"The number of correlation violations is {value:.3g}. The test threshold is {self.get_condition()}."


@default_renderer(wrap_type=TestCorrelationChanges)
class TestCorrelationChangesRenderer(TestRenderer):
    def render_html(self, obj: TestCorrelationChanges) -> TestHtmlInfo:
        info = super().render_html(obj)
        metric_result = obj.metric.get_result()
        current_correlations = metric_result.current.correlation[obj.method]

        if metric_result.reference is not None:
            reference_correlations: Optional[pd.DataFrame] = metric_result.reference.correlation[obj.method]

        else:
            reference_correlations = None

        fig = plot_correlations(current_correlations, reference_correlations)
        info.with_details("Target-Features Correlations", plotly_figure(title="", figure=fig))
        return info


class BaseFeatureDataQualityMetricsTest(BaseDataQualityMetricsValueTest, ABC):
    column_name: str

    def __init__(
        self,
        column_name: str,
        eq: Optional[Numeric] = None,
        gt: Optional[Numeric] = None,
        gte: Optional[Numeric] = None,
        is_in: Optional[List[Union[Numeric, str, bool]]] = None,
        lt: Optional[Numeric] = None,
        lte: Optional[Numeric] = None,
        not_eq: Optional[Numeric] = None,
        not_in: Optional[List[Union[Numeric, str, bool]]] = None,
    ):
        self.column_name = column_name
        super().__init__(
            column_name=column_name,
            eq=eq,
            gt=gt,
            gte=gte,
            is_in=is_in,
            lt=lt,
            lte=lte,
            not_eq=not_eq,
            not_in=not_in,
        )

    def groups(self) -> Dict[str, str]:
        return {
            GroupingTypes.ByFeature.id: self.column_name,
        }

    def check(self):
        result = TestResult(name=self.name, description="The test was not launched", status=TestResult.SKIPPED)
        # features_stats = self.metric.get_result().features_stats.get_all_features()

        # if self.column_name not in features_stats:
        #     result.mark_as_fail(f"Feature '{self.column_name}' was not found")
        #     return result

        result = super().check()

        if self.value is None:
            result.mark_as_error(f"No value for the feature '{self.column_name}'")
            return result

        return result


class TestColumnValueMin(BaseFeatureDataQualityMetricsTest):
    name = "Min Value"

    def get_condition(self) -> TestValueCondition:
        if self.condition.has_condition():
            return self.condition

        ref_features_stats = self.metric.get_result().reference_characteristics
        if ref_features_stats is not None:
            if not isinstance(ref_features_stats, NumericCharacteristics):
                raise ValueError(f"{self.column_name} should be numerical or bool")
            min_value = ref_features_stats.min
            return TestValueCondition(gte=min_value)
        raise ValueError("Neither required test parameters nor reference data has been provided.")

    def calculate_value_for_test(self) -> Optional[Union[Numeric, bool]]:
        features_stats = self.metric.get_result().current_characteristics
        if not isinstance(features_stats, NumericCharacteristics):
            raise ValueError(f"{self.column_name} should be numerical or bool")
        min_value = features_stats.min
        return min_value

    def get_description(self, value: Numeric) -> str:
        return f"The minimum value of the column **{self.column_name}** is {value} The test threshold is {self.get_condition()}."


@default_renderer(wrap_type=TestColumnValueMin)
class TestColumnValueMinRenderer(TestRenderer):
    def render_html(self, obj: TestColumnValueMin) -> TestHtmlInfo:
        column_name = obj.column_name
        info = super().render_html(obj)
        curr_distr = obj.metric.get_result().plot_data.bins_for_hist["current"]
        ref_distr = None
        if "reference" in obj.metric.get_result().plot_data.bins_for_hist.keys():
            ref_distr = obj.metric.get_result().plot_data.bins_for_hist["reference"]
        fig = plot_distr(hist_curr=curr_distr, hist_ref=ref_distr, color_options=self.color_options)
        fig = plot_check(fig, obj.get_condition(), color_options=self.color_options)
        current_characteristics = obj.metric.get_result().current_characteristics
        if not isinstance(current_characteristics, NumericCharacteristics):
            raise ValueError(f"{column_name} should be numerical or bool")
        min_value = current_characteristics.min

        if min_value is not None:
            fig = plot_metric_value(fig, float(min_value), f"current {column_name} min value")
        info.with_details(f"Min Value {column_name}", plotly_figure(title="", figure=fig))
        return info


class TestColumnValueMax(BaseFeatureDataQualityMetricsTest):
    name = "Max Value"

    def get_condition(self) -> TestValueCondition:
        if self.condition.has_condition():
            return self.condition
        ref_features_stats = self.metric.get_result().reference_characteristics
        if ref_features_stats is not None:
            if not isinstance(ref_features_stats, NumericCharacteristics):
                raise ValueError(f"{self.column_name} should be numerical or bool")
            max_value = ref_features_stats.max
            return TestValueCondition(lte=max_value)
        raise ValueError("Neither required test parameters nor reference data has been provided.")

    def calculate_value_for_test(self) -> Optional[Union[Numeric, bool]]:
        features_stats = self.metric.get_result().current_characteristics
        if not isinstance(features_stats, NumericCharacteristics):
            raise ValueError(f"{self.column_name} should be numerical or bool")
        max_value = features_stats.max
        if isinstance(max_value, str):
            raise ValueError(f"{self.column_name} should be numerical or bool")
        return max_value

    def get_description(self, value: Numeric) -> str:
        return f"The maximum value of the column **{self.column_name}** is {value}. The test threshold is {self.get_condition()}."


@default_renderer(wrap_type=TestColumnValueMax)
class TestColumnValueMaxRenderer(TestRenderer):
    def render_html(self, obj: TestColumnValueMax) -> TestHtmlInfo:
        column_name = obj.column_name
        info = super().render_html(obj)
        curr_distr = obj.metric.get_result().plot_data.bins_for_hist["current"]
        ref_distr = None
        if "reference" in obj.metric.get_result().plot_data.bins_for_hist.keys():
            ref_distr = obj.metric.get_result().plot_data.bins_for_hist["reference"]
        fig = plot_distr(hist_curr=curr_distr, hist_ref=ref_distr, color_options=self.color_options)
        fig = plot_check(fig, obj.get_condition(), color_options=self.color_options)
        current_characteristics = obj.metric.get_result().current_characteristics
        if not isinstance(current_characteristics, NumericCharacteristics):
            raise ValueError(f"{column_name} should be numerical or bool")
        max_value = current_characteristics.max

        if max_value is not None:
            fig = plot_metric_value(fig, float(max_value), f"current {column_name} max value")
        info.with_details(f"Max Value {column_name}", plotly_figure(title="", figure=fig))
        return info


class TestColumnValueMean(BaseFeatureDataQualityMetricsTest):
    name = "Mean Value"

    def get_condition(self) -> TestValueCondition:
        if self.condition.has_condition():
            return self.condition
        ref_features_stats = self.metric.get_result().reference_characteristics
        if ref_features_stats is not None:
            if not isinstance(ref_features_stats, NumericCharacteristics):
                raise ValueError(f"{self.column_name} should be numerical or bool")
            return TestValueCondition(eq=approx(ref_features_stats.mean, 0.1))
        raise ValueError("Neither required test parameters nor reference data has been provided.")

    def calculate_value_for_test(self) -> Optional[Numeric]:
        features_stats = self.metric.get_result().current_characteristics
        if not isinstance(features_stats, NumericCharacteristics):
            raise ValueError(f"{self.column_name} should be numerical or bool")
        return features_stats.mean

    def get_description(self, value: Numeric) -> str:
        return f"The mean value of the column **{self.column_name}** is {value:.3g}. The test threshold is {self.get_condition()}."


@default_renderer(wrap_type=TestColumnValueMean)
class TestColumnValueMeanRenderer(TestRenderer):
    def render_html(self, obj: TestColumnValueMean) -> TestHtmlInfo:
        column_name = obj.column_name
        info = super().render_html(obj)
        curr_distr = obj.metric.get_result().plot_data.bins_for_hist["current"]
        ref_distr = None
        if "reference" in obj.metric.get_result().plot_data.bins_for_hist.keys():
            ref_distr = obj.metric.get_result().plot_data.bins_for_hist["reference"]
        fig = plot_distr(hist_curr=curr_distr, hist_ref=ref_distr, color_options=self.color_options)
        fig = plot_check(fig, obj.get_condition(), color_options=self.color_options)
        current_characteristics = obj.metric.get_result().current_characteristics
        if not isinstance(current_characteristics, NumericCharacteristics):
            raise ValueError(f"{column_name} should be numerical or bool")
        mean_value = current_characteristics.mean

        if mean_value is not None:
            fig = plot_metric_value(fig, mean_value, f"current {column_name} mean value")
        info.with_details(f"Mean Value {column_name}", plotly_figure(title="", figure=fig))
        return info


class TestColumnValueMedian(BaseFeatureDataQualityMetricsTest):
    name = "Median Value"

    def get_condition(self) -> TestValueCondition:
        if self.condition.has_condition():
            return self.condition
        ref_features_stats = self.metric.get_result().reference_characteristics
        if ref_features_stats is not None:
            if not isinstance(ref_features_stats, NumericCharacteristics):
                raise ValueError(f"{self.column_name} should be numerical or bool")
            return TestValueCondition(eq=approx(ref_features_stats.p50, 0.1))
        raise ValueError("Neither required test parameters nor reference data has been provided.")

    def calculate_value_for_test(self) -> Optional[Numeric]:
        features_stats = self.metric.get_result().current_characteristics
        if not isinstance(features_stats, NumericCharacteristics):
            raise ValueError(f"{self.column_name} should be numerical or bool")
        return features_stats.p50

    def get_description(self, value: Numeric) -> str:
        return f"The median value of the column **{self.column_name}** is {value:.3g}. The test threshold is {self.get_condition()}."


@default_renderer(wrap_type=TestColumnValueMedian)
class TestColumnValueMedianRenderer(TestRenderer):
    def render_html(self, obj: TestColumnValueMedian) -> TestHtmlInfo:
        column_name = obj.column_name
        info = super().render_html(obj)
        curr_distr = obj.metric.get_result().plot_data.bins_for_hist["current"]
        ref_distr = None

        if "reference" in obj.metric.get_result().plot_data.bins_for_hist.keys():
            ref_distr = obj.metric.get_result().plot_data.bins_for_hist["reference"]

        fig = plot_distr(hist_curr=curr_distr, hist_ref=ref_distr, color_options=self.color_options)
        fig = plot_check(fig, obj.get_condition(), color_options=self.color_options)
        current_characteristics = obj.metric.get_result().current_characteristics
        if not isinstance(current_characteristics, NumericCharacteristics):
            raise ValueError(f"{column_name} should be numerical or bool")
        percentile_50 = current_characteristics.p50

        if percentile_50 is not None:
            fig = plot_metric_value(fig, percentile_50, f"current {column_name} median value")
        info.with_details(f"Median Value {column_name}", plotly_figure(title="", figure=fig))
        return info


class TestColumnValueStd(BaseFeatureDataQualityMetricsTest):
    name = "Standard Deviation (SD)"

    def get_condition(self) -> TestValueCondition:
        if self.condition.has_condition():
            return self.condition
        ref_features_stats = self.metric.get_result().reference_characteristics
        if ref_features_stats is not None:
            if not isinstance(ref_features_stats, NumericCharacteristics):
                raise ValueError(f"{self.column_name} should be numerical or bool")
            return TestValueCondition(eq=approx(ref_features_stats.std, 0.1))
        raise ValueError("Neither required test parameters nor reference data has been provided.")

    def calculate_value_for_test(self) -> Optional[Numeric]:
        features_stats = self.metric.get_result().current_characteristics
        if not isinstance(features_stats, NumericCharacteristics):
            raise ValueError(f"{self.column_name} should be numerical or bool")
        return features_stats.std

    def get_description(self, value: Numeric) -> str:
        return (
            f"The standard deviation of the column **{self.column_name}** is {value:.3g}. "
            f"The test threshold is {self.get_condition()}."
        )


@default_renderer(wrap_type=TestColumnValueStd)
class TestColumnValueStdRenderer(TestRenderer):
    def render_html(self, obj: TestColumnValueStd) -> TestHtmlInfo:
        column_name = obj.column_name
        info = super().render_html(obj)
        curr_distr = obj.metric.get_result().plot_data.bins_for_hist["current"]
        ref_distr = None
        if "reference" in obj.metric.get_result().plot_data.bins_for_hist.keys():
            ref_distr = obj.metric.get_result().plot_data.bins_for_hist["reference"]
        fig = plot_distr(hist_curr=curr_distr, hist_ref=ref_distr, color_options=self.color_options)
        info.with_details(f"Std Value {column_name}", plotly_figure(title="", figure=fig))
        return info


class TestNumberOfUniqueValues(BaseFeatureDataQualityMetricsTest):
    name = "Number of Unique Values"

    def get_condition(self) -> TestValueCondition:
        if self.condition.has_condition():
            return self.condition

        reference_features_stats = self.metric.get_result().reference_characteristics
        if reference_features_stats is not None:
            unique_count = reference_features_stats.unique
            return TestValueCondition(eq=approx(unique_count, relative=0.1))
        return TestValueCondition(gt=1)

    def calculate_value_for_test(self) -> Optional[Numeric]:
        features_stats = self.metric.get_result().current_characteristics
        return features_stats.unique

    def get_description(self, value: Numeric) -> str:
        return (
            f"The number of the unique values in the column **{self.column_name}** is {value}. "
            f"The test threshold is {self.get_condition()}."
        )


@default_renderer(wrap_type=TestNumberOfUniqueValues)
class TestNumberOfUniqueValuesRenderer(TestRenderer):
    def render_html(self, obj: TestNumberOfUniqueValues) -> TestHtmlInfo:
        info = super().render_html(obj)
        column_name = obj.column_name
        counts_data = obj.metric.get_result().plot_data.counts_of_values
        if counts_data is not None:
            curr_df = counts_data["current"]
            ref_df = None
            if "reference" in counts_data.keys():
                ref_df = counts_data["reference"]
            info.details = plot_value_counts_tables_ref_curr(column_name, curr_df, ref_df, "num_of_unique_vals")

        return info


class TestUniqueValuesShare(BaseFeatureDataQualityMetricsTest):
    name = "Share of Unique Values"

    def get_condition(self) -> TestValueCondition:
        if self.condition.has_condition():
            return self.condition

        reference_features_stats = self.metric.get_result().reference_characteristics
        if reference_features_stats is not None:
            unique_percentage = reference_features_stats.unique_percentage

            if unique_percentage is not None:
                return TestValueCondition(eq=approx(unique_percentage / 100.0, relative=0.1))

        raise ValueError("Neither required test parameters nor reference data has been provided.")

    def calculate_value_for_test(self) -> Optional[Numeric]:
        features_stats = self.metric.get_result().current_characteristics
        unique_percentage = features_stats.unique_percentage

        if unique_percentage is None:
            return None

        return unique_percentage / 100.0

    def get_description(self, value: Numeric) -> str:
        return (
            f"The share of the unique values in the column **{self.column_name}** is {value:.3}. "
            f"The test threshold is {self.get_condition()}."
        )


@default_renderer(wrap_type=TestUniqueValuesShare)
class TestUniqueValuesShareRenderer(TestRenderer):
    def render_html(self, obj: TestUniqueValuesShare) -> TestHtmlInfo:
        info = super().render_html(obj)
        column_name = obj.column_name
        counts_data = obj.metric.get_result().plot_data.counts_of_values
        if counts_data is not None:
            curr_df = counts_data["current"]
            ref_df = None
            if "reference" in counts_data.keys():
                ref_df = counts_data["reference"]
            info.details = plot_value_counts_tables_ref_curr(column_name, curr_df, ref_df, "unique_vals_sare")

        return info


class TestMostCommonValueShare(BaseFeatureDataQualityMetricsTest):
    name = "Share of the Most Common Value"

    def get_condition(self) -> TestValueCondition:
        if self.condition.has_condition():
            return self.condition

        reference_features_stats = self.metric.get_result().reference_characteristics
        if reference_features_stats is not None:
            most_common_percentage = reference_features_stats.most_common_percentage

            if most_common_percentage is not None:
                return TestValueCondition(eq=approx(most_common_percentage / 100.0, relative=0.1))

        return TestValueCondition(lt=0.8)

    def calculate_value_for_test(self) -> Optional[Numeric]:
        features_stats = self.metric.get_result().current_characteristics
        most_common_percentage = features_stats.most_common_percentage

        if most_common_percentage is None:
            return None

        return most_common_percentage / 100.0

    def get_description(self, value: Numeric) -> str:
        counts_data = self.metric.get_result().plot_data.counts_of_values
        if counts_data is None:
            raise ValueError("counts_of_values should be provided")
        most_common_value = counts_data["current"].iloc[0, 0]
        return (
            f"The most common value in the column **{self.column_name}** is {most_common_value}. "
            f"Its share is {value:.3g}. "
            f"The test threshold is {self.get_condition()}."
        )


@default_renderer(wrap_type=TestMostCommonValueShare)
class TestMostCommonValueShareRenderer(TestRenderer):
    def render_json(self, obj: TestMostCommonValueShare) -> dict:
        base = super().render_json(obj)
        base["parameters"]["condition"] = obj.get_condition().as_dict()
        base["parameters"]["column_name"] = obj.column_name
        base["parameters"]["share_most_common_value"] = obj.value
        return base

    def render_html(self, obj: TestMostCommonValueShare) -> TestHtmlInfo:
        info = super().render_html(obj)
        column_name = obj.column_name

        if column_name is None:
            raise ValueError("column_name should be present")

        counts_data = obj.metric.get_result().plot_data.counts_of_values
        if counts_data is not None:
            curr_df = counts_data["current"]
            ref_df = None
            if "reference" in counts_data.keys():
                ref_df = counts_data["reference"]
            additional_plots = plot_value_counts_tables_ref_curr(column_name, curr_df, ref_df, "most_common_value_sare")
            info.details = additional_plots
        return info


class TestAllColumnsMostCommonValueShare(BaseGenerator):
    """Creates most common value share tests for each column in the dataset"""

    columns: Optional[List[str]]

    def __init__(self, columns: Optional[List[str]] = None):
        self.columns = columns

    def generate(self, columns_info: DatasetColumns) -> List[TestMostCommonValueShare]:
        if self.columns is None:
            columns = columns_info.get_all_columns_list()

        else:
            columns = self.columns

        return [TestMostCommonValueShare(column_name=name) for name in columns]


class TestMeanInNSigmas(Test):
    group = DATA_QUALITY_GROUP.id
    name = "Mean Value Stability"
    metric: ColumnSummaryMetric
    column_name: str
    n_sigmas: int

    def __init__(self, column_name: str, n_sigmas: int = 2):
        self.column_name = column_name
        self.n_sigmas = n_sigmas
        self.metric = ColumnSummaryMetric(column_name)

    def check(self):
        reference_feature_stats = self.metric.get_result().reference_characteristics
        features_stats = self.metric.get_result().current_characteristics

        if reference_feature_stats is None:
            test_result = TestResult.ERROR
            description = "Reference should be present"

        else:
            current_mean = features_stats.mean
            reference_mean = reference_feature_stats.mean
            reference_std = reference_feature_stats.std
            sigmas_value = reference_std * self.n_sigmas
            left_condition = reference_mean - sigmas_value
            right_condition = reference_mean + sigmas_value

            if left_condition < current_mean < right_condition:
                description = (
                    f"The mean value of the column **{self.column_name}** is {current_mean:.3g}."
                    f" The expected range is from {left_condition:.3g} to {right_condition:.3g}"
                )
                test_result = TestResult.SUCCESS

            else:
                description = (
                    f"The mean value of the column **{self.column_name}** is {current_mean:.3g}."
                    f" The expected range is from {left_condition:.3g} to {right_condition:.3g}"
                )
                test_result = TestResult.FAIL

        return TestResult(
            name=self.name,
            description=description,
            status=test_result,
            groups={GroupingTypes.ByFeature.id: self.column_name},
        )


@default_renderer(wrap_type=TestMeanInNSigmas)
class TestMeanInNSigmasRenderer(TestRenderer):
    def render_json(self, obj: TestMeanInNSigmas) -> dict:
        base = super().render_json(obj)
        metric_result = obj.metric.get_result()
        base["parameters"]["column_name"] = obj.column_name
        base["parameters"]["n_sigmas"] = obj.n_sigmas
        if not isinstance(metric_result.current_characteristics, NumericCharacteristics):
            raise ValueError(f"{obj.column_name} should be numerical or bool")
        base["parameters"]["current_mean"] = metric_result.current_characteristics.mean

        if metric_result.reference_characteristics is not None:
            if not isinstance(metric_result.reference_characteristics, NumericCharacteristics):
                raise ValueError(f"{obj.column_name} should be numerical or bool")
            base["parameters"]["reference_mean"] = metric_result.reference_characteristics.mean
            base["parameters"]["reference_std"] = metric_result.reference_characteristics.std
        return base

    def render_html(self, obj: TestMeanInNSigmas) -> TestHtmlInfo:
        column_name = obj.column_name
        metric_result = obj.metric.get_result()
        info = super().render_html(obj)

        if metric_result.reference_characteristics is None:
            return info

        if not isinstance(metric_result.reference_characteristics, NumericCharacteristics):
            raise ValueError(f"{column_name} should be numerical or bool")
        ref_mean = metric_result.reference_characteristics.mean
        ref_std = metric_result.reference_characteristics.std

        if ref_std is None or ref_mean is None:
            raise ValueError("No mean or std for reference")

        gt = ref_mean - obj.n_sigmas * ref_std
        lt = ref_mean + obj.n_sigmas * ref_std
        ref_condition = TestValueCondition(gt=gt, lt=lt)
        curr_distr = metric_result.plot_data.bins_for_hist["current"]
        ref_distr = None

        if "reference" in metric_result.plot_data.bins_for_hist.keys():
            ref_distr = metric_result.plot_data.bins_for_hist["reference"]

        fig = plot_distr(hist_curr=curr_distr, hist_ref=ref_distr, color_options=self.color_options)
        fig = plot_check(fig, ref_condition, color_options=self.color_options)
        if not isinstance(metric_result.current_characteristics, NumericCharacteristics):
            raise ValueError(f"{obj.column_name} should be numerical or bool")
        mean_value = metric_result.current_characteristics.mean

        if mean_value is not None:
            fig = plot_metric_value(fig, mean_value, f"current {column_name} mean value")

        info.with_details("", plotly_figure(title="", figure=fig))
        return info


class TestNumColumnsMeanInNSigmas(BaseGenerator):
    """Create tests of mean for all numeric columns"""

    columns: Optional[List[str]]

    def __init__(self, columns: Optional[List[str]] = None):
        self.columns = columns

    def generate(self, columns_info: DatasetColumns) -> List[TestMeanInNSigmas]:
        if self.columns is None:
            columns = columns_info.num_feature_names

        else:
            columns = [column for column in self.columns if column in columns_info.num_feature_names]

        return [TestMeanInNSigmas(column_name=name, n_sigmas=2) for name in columns]


class TestValueRange(Test):
    group = DATA_QUALITY_GROUP.id
    name = "Value Range"
    metric: ColumnValueRangeMetric
    column: str
    left: Optional[float]
    right: Optional[float]

    def __init__(
        self,
        column_name: str,
        left: Optional[float] = None,
        right: Optional[float] = None,
    ):
        self.column_name = column_name
        self.left = left
        self.right = right
        self.metric = ColumnValueRangeMetric(column_name=column_name, left=left, right=right)

    def check(self):
        number_not_in_range = self.metric.get_result().current.number_not_in_range

        if number_not_in_range > 0:
            description = f"The column **{self.column_name}** has values out of range."
            test_result = TestResult.FAIL
        else:
            description = f"All values in the column **{self.column_name}** are within range"
            test_result = TestResult.SUCCESS

        return TestResult(
            name=self.name,
            description=description,
            status=test_result,
            groups={GroupingTypes.ByFeature.id: self.column_name},
        )


@default_renderer(wrap_type=TestValueRange)
class TestValueRangeRenderer(TestRenderer):
    def render_html(self, obj: TestValueRange) -> TestHtmlInfo:
        column_name = obj.column_name
        metric_result = obj.metric.get_result()
        condition_ = TestValueCondition(gt=metric_result.left, lt=metric_result.right)
        info = super().render_html(obj)
        fig = get_distribution_plot_figure(
            current_distribution=metric_result.current_distribution,
            reference_distribution=metric_result.reference_distribution,
            color_options=self.color_options,
        )
        fig = plot_check(fig, condition_, color_options=self.color_options)
        info.with_details(f"Value Range {column_name}", plotly_figure(title="", figure=fig))
        return info


class BaseDataQualityValueRangeMetricsTest(BaseCheckValueTest, ABC):
    group = DATA_QUALITY_GROUP.id
    metric: ColumnValueRangeMetric
    column: str
    left: Optional[float]
    right: Optional[float]

    def __init__(
        self,
        column_name: str,
        left: Optional[float] = None,
        right: Optional[float] = None,
        eq: Optional[Numeric] = None,
        gt: Optional[Numeric] = None,
        gte: Optional[Numeric] = None,
        is_in: Optional[List[Union[Numeric, str, bool]]] = None,
        lt: Optional[Numeric] = None,
        lte: Optional[Numeric] = None,
        not_eq: Optional[Numeric] = None,
        not_in: Optional[List[Union[Numeric, str, bool]]] = None,
    ):
        self.column_name = column_name
        self.left = left
        self.right = right
        self.metric = ColumnValueRangeMetric(column_name=column_name, left=left, right=right)

        super().__init__(eq=eq, gt=gt, gte=gte, is_in=is_in, lt=lt, lte=lte, not_eq=not_eq, not_in=not_in)

    def groups(self) -> Dict[str, str]:
        return {GroupingTypes.ByFeature.id: self.column_name}


class TestNumberOfOutRangeValues(BaseDataQualityValueRangeMetricsTest):
    name = "Number of Out-of-Range Values "

    def get_condition(self) -> TestValueCondition:
        if self.condition.has_condition():
            return self.condition
        return TestValueCondition(eq=approx(0))

    def calculate_value_for_test(self) -> Numeric:
        return self.metric.get_result().current.number_not_in_range

    def get_description(self, value: Numeric) -> str:
        return (
            f"The number of values out of range in the column **{self.column_name}** is {value}. "
            f" The test threshold is {self.get_condition()}."
        )


@default_renderer(wrap_type=TestNumberOfOutRangeValues)
class TestNumberOfOutRangeValuesRenderer(TestRenderer):
    def render_html(self, obj: TestNumberOfOutRangeValues) -> TestHtmlInfo:
        column_name = obj.column_name
        metric_result = obj.metric.get_result()
        info = super().render_html(obj)
        fig = get_distribution_plot_figure(
            current_distribution=metric_result.current_distribution,
            reference_distribution=metric_result.reference_distribution,
            color_options=self.color_options,
        )
        fig = plot_check(fig, obj.condition, color_options=self.color_options)
        info.with_details(f"Number Out of Range for {column_name}", plotly_figure(title="", figure=fig))
        return info


class TestShareOfOutRangeValues(BaseDataQualityValueRangeMetricsTest):
    name = "Share of Out-of-Range Values"

    def get_condition(self) -> TestValueCondition:
        if self.condition.has_condition():
            return self.condition
        return TestValueCondition(eq=approx(0))

    def calculate_value_for_test(self) -> Numeric:
        return self.metric.get_result().current.share_not_in_range

    def get_description(self, value: Numeric) -> str:
        current_result = self.metric.get_result().current
        return (
            f"The share of values out of range in the column **{self.column_name}** is {value:.3g} "
            f"({current_result.number_not_in_range} out of {current_result.number_of_values}). "
            f" The test threshold is {self.get_condition()}."
        )


@default_renderer(wrap_type=TestShareOfOutRangeValues)
class TestShareOfOutRangeValuesRenderer(TestRenderer):
    def render_json(self, obj: TestShareOfOutRangeValues) -> dict:
        base = super().render_json(obj)
        base["parameters"]["condition"] = obj.get_condition().as_dict()
        base["parameters"]["left"] = obj.left
        base["parameters"]["right"] = obj.right
        base["parameters"]["share_not_in_range"] = obj.value
        return base

    def render_html(self, obj: TestShareOfOutRangeValues) -> TestHtmlInfo:
        column_name = obj.column_name
        metric_result = obj.metric.get_result()
        info = super().render_html(obj)
        fig = get_distribution_plot_figure(
            current_distribution=metric_result.current_distribution,
            reference_distribution=metric_result.reference_distribution,
            color_options=self.color_options,
        )
        fig = plot_check(fig, obj.condition, color_options=self.color_options)
        info.with_details(f"Share Out of Range for {column_name}", plotly_figure(title="", figure=fig))
        return info


class TestNumColumnsOutOfRangeValues(BaseGenerator):
    """Creates share of out of range values tests for all numeric columns"""

    columns: Optional[List[str]]

    def __init__(self, columns: Optional[List[str]] = None):
        self.columns = columns

    def generate(self, columns_info: DatasetColumns) -> List[TestShareOfOutRangeValues]:
        if self.columns is None:
            columns = columns_info.num_feature_names

        else:
            columns = [column for column in self.columns if column in columns_info.num_feature_names]

        return [TestShareOfOutRangeValues(column_name=name) for name in columns]


class TestValueList(Test):
    group = DATA_QUALITY_GROUP.id
    name = "Out-of-List Values"
    metric: ColumnValueListMetric
    column_name: str
    values: Optional[list]

    def __init__(self, column_name: str, values: Optional[list] = None):
        self.column_name = column_name
        self.values = values
        self.metric = ColumnValueListMetric(column_name=column_name, values=values)

    def check(self):
        metric_result = self.metric.get_result()

        if metric_result.current.number_not_in_list > 0:
            test_result = TestResult.FAIL
            description = f"The column **{self.column_name}** has values out of list."

        else:
            test_result = TestResult.SUCCESS
            description = f"All values in the column **{self.column_name}** are in the list."

        return TestResult(
            name=self.name,
            description=description,
            status=test_result,
            groups={GroupingTypes.ByFeature.id: self.column_name},
        )


@default_renderer(wrap_type=TestValueList)
class TestValueListRenderer(TestRenderer):
    def render_json(self, obj: TestValueList) -> dict:
        base = super().render_json(obj)
        base["parameters"]["column_name"] = obj.column_name
        base["parameters"]["values"] = obj.values
        base["parameters"]["number_not_in_list"] = obj.metric.get_result().current.number_not_in_list
        return base

    def render_html(self, obj: TestValueList) -> TestHtmlInfo:
        info = super().render_html(obj)
        metric_result = obj.metric.get_result()
        column_name = metric_result.column_name
        values = metric_result.values
        curr_df = pd.DataFrame(metric_result.current.values_in_list.items(), columns=["x", "count"])

        if metric_result.reference is not None:
            ref_df = pd.DataFrame(metric_result.reference.values_in_list.items(), columns=["x", "count"])

        else:
            ref_df = None

        additional_plots = plot_value_counts_tables(column_name, values, curr_df, ref_df, "value_list")
        info.details = additional_plots
        return info


class BaseDataQualityValueListMetricsTest(BaseCheckValueTest, ABC):
    group = DATA_QUALITY_GROUP.id
    metric: ColumnValueListMetric
    column_name: str
    values: Optional[list]

    def __init__(
        self,
        column_name: str,
        values: Optional[list] = None,
        eq: Optional[Numeric] = None,
        gt: Optional[Numeric] = None,
        gte: Optional[Numeric] = None,
        is_in: Optional[List[Union[Numeric, str, bool]]] = None,
        lt: Optional[Numeric] = None,
        lte: Optional[Numeric] = None,
        not_eq: Optional[Numeric] = None,
        not_in: Optional[List[Union[Numeric, str, bool]]] = None,
    ):
        self.column_name = column_name
        self.values = values
        super().__init__(eq=eq, gt=gt, gte=gte, is_in=is_in, lt=lt, lte=lte, not_eq=not_eq, not_in=not_in)
        self.metric = ColumnValueListMetric(column_name=column_name, values=values)

    def groups(self) -> Dict[str, str]:
        return {GroupingTypes.ByFeature.id: self.column_name}


class TestNumberOfOutListValues(BaseDataQualityValueListMetricsTest):
    name = "Number Out-of-List Values"

    def get_condition(self) -> TestValueCondition:
        if self.condition.has_condition():
            return self.condition
        return TestValueCondition(eq=approx(0))

    def calculate_value_for_test(self) -> Numeric:
        return self.metric.get_result().current.number_not_in_list

    def get_description(self, value: Numeric) -> str:
        return (
            f"The number of values out of list in the column **{self.column_name}** is {value}. "
            f"The test threshold is {self.get_condition()}."
        )


@default_renderer(wrap_type=TestNumberOfOutListValues)
class TestNumberOfOutListValuesRenderer(TestRenderer):
    def render_html(self, obj: TestNumberOfOutListValues) -> TestHtmlInfo:
        info = super().render_html(obj)
        metric_result = obj.metric.get_result()
        column_name = metric_result.column_name
        values = metric_result.values
        curr_df = pd.DataFrame(metric_result.current.values_in_list.items(), columns=["x", "count"])

        if metric_result.reference is not None:
            ref_df = pd.DataFrame(metric_result.reference.values_in_list.items(), columns=["x", "count"])

        else:
            ref_df = None

        additional_plots = plot_value_counts_tables(column_name, values, curr_df, ref_df, "number_value_list")
        info.details = additional_plots
        return info


class TestShareOfOutListValues(BaseDataQualityValueListMetricsTest):
    name = "Share of Out-of-List Values"

    def get_condition(self) -> TestValueCondition:
        if self.condition.has_condition():
            return self.condition
        return TestValueCondition(eq=approx(0))

    def calculate_value_for_test(self) -> Numeric:
        return self.metric.get_result().current.share_not_in_list

    def get_description(self, value: Numeric) -> str:
        metric_result = self.metric.get_result()
        number_not_in_range = metric_result.current.number_not_in_list
        rows_count = metric_result.current.rows_count
        return (
            f"The share of values out of list in the column **{self.column_name}** is {value:.3g} "
            f"({number_not_in_range} out of {rows_count}). "
            f"The test threshold is {self.get_condition()}."
        )


class TestCatColumnsOutOfListValues(BaseGenerator):
    """Create share of out of list values tests for category columns"""

    columns: Optional[List[str]]

    def __init__(self, columns: Optional[List[str]] = None):
        self.columns = columns

    def generate(self, columns_info: DatasetColumns) -> List[TestShareOfOutListValues]:
        if self.columns is None:
            columns = columns_info.cat_feature_names

        else:
            columns = [column for column in self.columns if column in columns_info.cat_feature_names]

        return [TestShareOfOutListValues(column_name=name) for name in columns]


class TestColumnQuantile(BaseCheckValueTest):
    group = DATA_QUALITY_GROUP.id
    name = "Quantile Value"
    metric: ColumnQuantileMetric
    column_name: str
    quantile: float

    def __init__(
        self,
        column_name: str,
        quantile: float,
        eq: Optional[Numeric] = None,
        gt: Optional[Numeric] = None,
        gte: Optional[Numeric] = None,
        is_in: Optional[List[Union[Numeric, str, bool]]] = None,
        lt: Optional[Numeric] = None,
        lte: Optional[Numeric] = None,
        not_eq: Optional[Numeric] = None,
        not_in: Optional[List[Union[Numeric, str, bool]]] = None,
    ):
        self.column_name = column_name
        self.quantile = quantile
        super().__init__(eq=eq, gt=gt, gte=gte, is_in=is_in, lt=lt, lte=lte, not_eq=not_eq, not_in=not_in)
        self.metric = ColumnQuantileMetric(column_name=column_name, quantile=quantile)

    def groups(self) -> Dict[str, str]:
        return {GroupingTypes.ByFeature.id: self.column_name}

    def get_condition(self) -> TestValueCondition:
        if self.condition.has_condition():
            return self.condition

        reference_value = self.metric.get_result().reference

        if reference_value is not None:
            return TestValueCondition(eq=approx(reference_value, 0.1))

        raise ValueError("Neither required test parameters nor reference data has been provided.")

    def calculate_value_for_test(self) -> Numeric:
        return self.metric.get_result().current

    def get_description(self, value: Numeric) -> str:
        return (
            f"The {self.quantile} quantile value of the column **{self.column_name}** is {value:.3g}. "
            f"The test threshold is {self.get_condition()}."
        )


@default_renderer(wrap_type=TestColumnQuantile)
class TestColumnQuantileRenderer(TestRenderer):
    def render_html(self, obj: TestColumnQuantile) -> TestHtmlInfo:
        info = super().render_html(obj)
        metric_result = obj.metric.get_result()
        column_name = metric_result.column_name
        fig = get_distribution_plot_figure(
            current_distribution=metric_result.current_distribution,
            reference_distribution=metric_result.reference_distribution,
            color_options=self.color_options,
        )
        fig = plot_check(fig, obj.get_condition(), color_options=self.color_options)
        fig = plot_metric_value(
            fig, obj.metric.get_result().current, f"current {column_name} {metric_result.quantile} quantile"
        )
        info.with_details("", plotly_figure(title="", figure=fig))
        return info


@default_renderer(wrap_type=TestShareOfOutListValues)
class TestShareOfOutListValuesRenderer(TestRenderer):
    def render_json(self, obj: TestShareOfOutListValues) -> dict:
        base = super().render_json(obj)
        base["parameters"]["condition"] = obj.get_condition().as_dict()
        base["parameters"]["values"] = obj.values
        base["parameters"]["share_not_in_list"] = obj.value
        return base

    def render_html(self, obj: TestShareOfOutListValues) -> TestHtmlInfo:
        info = super().render_html(obj)
        metric_result = obj.metric.get_result()
        column_name = metric_result.column_name
        values = metric_result.values
        curr_df = pd.DataFrame(metric_result.current.values_in_list.items(), columns=["x", "count"])

        if metric_result.reference is not None:
            ref_df = pd.DataFrame(metric_result.reference.values_in_list.items(), columns=["x", "count"])

        else:
            ref_df = None

        additional_plots = plot_value_counts_tables(column_name, values, curr_df, ref_df, "share_value_list")
        info.details = additional_plots
        return info
