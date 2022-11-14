from abc import ABC
from typing import List
from typing import Optional
from typing import Union

from evidently.metrics import RegressionDummyMetric
from evidently.metrics import RegressionQualityMetric
from evidently.renderers.base_renderer import TestHtmlInfo
from evidently.renderers.base_renderer import TestRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import plotly_figure
from evidently.renderers.render_utils import plot_distr
from evidently.tests.base_test import BaseCheckValueTest
from evidently.tests.base_test import GroupData
from evidently.tests.base_test import GroupingTypes
from evidently.tests.base_test import TestValueCondition
from evidently.tests.utils import approx
from evidently.tests.utils import plot_check
from evidently.tests.utils import plot_metric_value
from evidently.tests.utils import regression_perf_plot
from evidently.utils.types import Numeric

REGRESSION_GROUP = GroupData("regression", "Regression", "")
GroupingTypes.TestGroup.add_value(REGRESSION_GROUP)


class BaseRegressionPerformanceMetricsTest(BaseCheckValueTest, ABC):
    group = REGRESSION_GROUP.id
    metric: RegressionQualityMetric
    dummy_metric: RegressionDummyMetric

    def __init__(
        self,
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
        self.metric = RegressionQualityMetric()
        self.dummy_metric = RegressionDummyMetric()


class TestValueMAE(BaseRegressionPerformanceMetricsTest):
    name = "Mean Absolute Error (MAE)"

    def get_condition(self) -> TestValueCondition:
        if self.condition.has_condition():
            return self.condition
        ref_mae = self.metric.get_result().mean_abs_error_ref
        if ref_mae is not None:
            return TestValueCondition(eq=approx(ref_mae, relative=0.1))
        return TestValueCondition(lt=self.dummy_metric.get_result().mean_abs_error_default)

    def calculate_value_for_test(self) -> Numeric:
        return self.metric.get_result().mean_abs_error

    def get_description(self, value: Numeric) -> str:
        return f"The MAE is {value:.3}. The test threshold is {self.get_condition()}"


@default_renderer(wrap_type=TestValueMAE)
class TestValueMAERenderer(TestRenderer):
    def render_json(self, obj: TestValueMAE) -> dict:
        base = super().render_json(obj)
        metric_result = obj.metric.get_result()
        base["parameters"]["condition"] = obj.get_condition().as_dict()
        base["parameters"]["mean_abs_error"] = metric_result.mean_abs_error
        base["parameters"]["mean_abs_error_ref"] = metric_result.mean_abs_error_ref
        return base

    def render_html(self, obj: TestValueMAE) -> TestHtmlInfo:
        info = super().render_html(obj)
        is_ref_data = False

        if "reference" in obj.metric.get_result().hist_for_plot.keys():
            is_ref_data = True

        fig = regression_perf_plot(
            val_for_plot=obj.metric.get_result().vals_for_plots["mean_abs_error"],
            hist_for_plot=obj.metric.get_result().hist_for_plot,
            name="MAE",
            curr_metric=obj.metric.get_result().mean_abs_error,
            ref_metric=obj.metric.get_result().mean_abs_error_ref,
            is_ref_data=is_ref_data,
            color_options=self.color_options,
        )
        info.with_details("MAE", plotly_figure(title="", figure=fig))
        return info


class TestValueMAPE(BaseRegressionPerformanceMetricsTest):
    name = "Mean Absolute Percentage Error (MAPE)"

    def get_condition(self) -> TestValueCondition:
        if self.condition.has_condition():
            return self.condition
        ref_mae = self.metric.get_result().mean_abs_perc_error_ref
        if ref_mae is not None:
            return TestValueCondition(eq=approx(ref_mae, relative=0.1))
        return TestValueCondition(lt=self.dummy_metric.get_result().mean_abs_perc_error_default)

    def calculate_value_for_test(self) -> Numeric:
        return self.metric.get_result().mean_abs_perc_error

    def get_description(self, value: Numeric) -> str:
        return f"The MAPE is {value:.3}. The test threshold is {self.get_condition()}."


@default_renderer(wrap_type=TestValueMAPE)
class TestValueMAPERenderer(TestRenderer):
    def render_json(self, obj: TestValueMAPE) -> dict:
        base = super().render_json(obj)
        metric_result = obj.metric.get_result()
        base["parameters"]["condition"] = obj.get_condition().as_dict()
        base["parameters"]["mean_abs_perc_error"] = metric_result.mean_abs_perc_error
        base["parameters"]["mean_abs_perc_error_ref"] = metric_result.mean_abs_perc_error_ref
        base["parameters"]["mean_abs_perc_error_default"] = metric_result.mean_abs_perc_error_default
        return base

    def render_html(self, obj: TestValueMAPE) -> TestHtmlInfo:
        info = super().render_html(obj)
        is_ref_data = False
        if "reference" in obj.metric.get_result().hist_for_plot.keys():
            is_ref_data = True
        val_for_plot = obj.metric.get_result().vals_for_plots["mean_abs_perc_error"]
        val_for_plot = {x: y * 100 for x, y in val_for_plot.items()}
        fig = regression_perf_plot(
            val_for_plot=val_for_plot,
            hist_for_plot=obj.metric.get_result().hist_for_plot,
            name="MAPE",
            curr_metric=obj.metric.get_result().mean_abs_perc_error,
            ref_metric=obj.metric.get_result().mean_abs_perc_error_ref,
            is_ref_data=is_ref_data,
            color_options=self.color_options,
        )
        info.with_details("MAPE", plotly_figure(title="", figure=fig))
        return info


class TestValueRMSE(BaseRegressionPerformanceMetricsTest):
    name = "Root Mean Square Error (RMSE)"

    def get_condition(self) -> TestValueCondition:
        if self.condition.has_condition():
            return self.condition
        rmse_ref = self.metric.get_result().rmse_ref
        if rmse_ref is not None:
            return TestValueCondition(eq=approx(rmse_ref, relative=0.1))
        return TestValueCondition(lt=self.dummy_metric.get_result().rmse_default)

    def calculate_value_for_test(self) -> Numeric:
        return self.metric.get_result().rmse

    def get_description(self, value: Numeric) -> str:
        return f"The RMSE is {value:.3}. The test threshold is {self.get_condition()}."


@default_renderer(wrap_type=TestValueRMSE)
class TestValueRMSERenderer(TestRenderer):
    def render_json(self, obj: TestValueRMSE) -> dict:
        base = super().render_json(obj)
        metric_result = obj.metric.get_result()
        base["parameters"]["condition"] = obj.get_condition().as_dict()
        base["parameters"]["rmse"] = metric_result.rmse
        base["parameters"]["rmse_ref"] = metric_result.rmse_ref
        base["parameters"]["rmse_default"] = metric_result.rmse_default
        return base

    def render_html(self, obj: TestValueRMSE) -> TestHtmlInfo:
        info = super().render_html(obj)
        is_ref_data = False
        if "reference" in obj.metric.get_result().hist_for_plot.keys():
            is_ref_data = True
        fig = regression_perf_plot(
            val_for_plot=obj.metric.get_result().vals_for_plots["rmse"],
            hist_for_plot=obj.metric.get_result().hist_for_plot,
            name="RMSE",
            curr_metric=obj.metric.get_result().rmse,
            ref_metric=obj.metric.get_result().rmse_ref,
            is_ref_data=is_ref_data,
            color_options=self.color_options,
        )
        info.with_details("RMSE", plotly_figure(title="", figure=fig))
        return info


class TestValueMeanError(BaseRegressionPerformanceMetricsTest):
    name = "Mean Error (ME)"

    def get_condition(self) -> TestValueCondition:
        if self.condition.has_condition():
            return self.condition
        return TestValueCondition(eq=approx(0, absolute=0.1 * self.metric.get_result().me_default_sigma))

    def calculate_value_for_test(self) -> Numeric:
        return self.metric.get_result().mean_error

    def get_description(self, value: Numeric) -> str:
        return f"The ME is {value:.3}. The test threshold is {self.get_condition()}."


@default_renderer(wrap_type=TestValueMeanError)
class TestValueMeanErrorRenderer(TestRenderer):
    def render_json(self, obj: TestValueMeanError) -> dict:
        base = super().render_json(obj)
        metric_result = obj.metric.get_result()
        base["parameters"]["condition"] = obj.get_condition().as_dict()
        base["parameters"]["mean_error"] = metric_result.mean_error
        return base

    def render_html(self, obj: TestValueMeanError) -> TestHtmlInfo:
        info = super().render_html(obj)
        me_hist_for_plot = obj.metric.get_result().me_hist_for_plot
        hist_curr = me_hist_for_plot["current"]
        hist_ref = None
        if "reference" in obj.metric.get_result().me_hist_for_plot.keys():
            hist_ref = me_hist_for_plot["reference"]
        fig = plot_distr(hist_curr=hist_curr, hist_ref=hist_ref, color_options=self.color_options)
        fig = plot_check(fig, obj.get_condition(), color_options=self.color_options)
        fig = plot_metric_value(fig, obj.metric.get_result().mean_error, "current mean error")
        info.with_details("", plotly_figure(title="", figure=fig))
        return info


class TestValueAbsMaxError(BaseRegressionPerformanceMetricsTest):
    name = "Max Absolute Error"

    def get_condition(self) -> TestValueCondition:
        if self.condition.has_condition():
            return self.condition
        abs_error_max_ref = self.metric.get_result().abs_error_max_ref
        if abs_error_max_ref is not None:
            return TestValueCondition(lte=approx(abs_error_max_ref, relative=0.1))
        return TestValueCondition(lte=self.dummy_metric.get_result().abs_error_max_default)

    def calculate_value_for_test(self) -> Numeric:
        return self.metric.get_result().abs_error_max

    def get_description(self, value: Numeric) -> str:
        return f"The Max Absolute Error is {value:.3}. The test threshold is {self.get_condition()}."


@default_renderer(wrap_type=TestValueAbsMaxError)
class TestValueAbsMaxErrorRenderer(TestRenderer):
    def render_json(self, obj: TestValueAbsMaxError) -> dict:
        base = super().render_json(obj)
        metric_result = obj.metric.get_result()
        base["parameters"]["condition"] = obj.get_condition().as_dict()
        base["parameters"]["abs_error_max"] = metric_result.abs_error_max
        base["parameters"]["abs_error_max_ref"] = metric_result.abs_error_max_ref
        base["parameters"]["abs_error_max_ref"] = metric_result.abs_error_max_default
        return base

    def render_html(self, obj: TestValueAbsMaxError) -> TestHtmlInfo:
        info = super().render_html(obj)
        me_hist_for_plot = obj.metric.get_result().me_hist_for_plot
        hist_curr = me_hist_for_plot["current"]
        hist_ref = None

        if "reference" in obj.metric.get_result().me_hist_for_plot.keys():
            hist_ref = me_hist_for_plot["reference"]

        fig = plot_distr(hist_curr=hist_curr, hist_ref=hist_ref, color_options=self.color_options)
        info.with_details("", plotly_figure(title="", figure=fig))
        return info


class TestValueR2Score(BaseRegressionPerformanceMetricsTest):
    name = "R2 Score"

    def get_condition(self) -> TestValueCondition:
        if self.condition.has_condition():
            return self.condition
        r2_score_ref = self.metric.get_result().r2_score_ref
        if r2_score_ref is not None:
            return TestValueCondition(eq=approx(r2_score_ref, relative=0.1))
        return TestValueCondition(gt=0)

    def calculate_value_for_test(self) -> Numeric:
        return self.metric.get_result().r2_score

    def get_description(self, value: Numeric) -> str:
        return f"The R2 score is {value:.3}. The test threshold is {self.get_condition()}."


@default_renderer(wrap_type=TestValueR2Score)
class TestValueR2ScoreRenderer(TestRenderer):
    def render_json(self, obj: TestValueAbsMaxError) -> dict:
        base = super().render_json(obj)
        metric_result = obj.metric.get_result()
        base["parameters"]["condition"] = obj.get_condition().as_dict()
        base["parameters"]["r2_score"] = metric_result.r2_score
        base["parameters"]["r2_score_ref"] = metric_result.r2_score_ref
        return base

    def render_html(self, obj: TestValueR2Score) -> TestHtmlInfo:
        info = super().render_html(obj)
        is_ref_data = False
        if "reference" in obj.metric.get_result().hist_for_plot.keys():
            is_ref_data = True
        fig = regression_perf_plot(
            val_for_plot=obj.metric.get_result().vals_for_plots["r2_score"],
            hist_for_plot=obj.metric.get_result().hist_for_plot,
            name="R2_score",
            curr_metric=obj.metric.get_result().r2_score,
            ref_metric=obj.metric.get_result().r2_score_ref,
            is_ref_data=is_ref_data,
            color_options=self.color_options,
        )
        info.with_details("R2 Score", plotly_figure(title="", figure=fig))
        return info
