from abc import ABC
from typing import List
from typing import Optional
from typing import Union

import numpy as np

from evidently.model.widget import BaseWidgetInfo
from evidently.metrics import RegressionPerformanceMetrics
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.base_renderer import TestRenderer
from evidently.renderers.base_renderer import TestHtmlInfo
from evidently.renderers.base_renderer import DetailsInfo
from evidently.tests.base_test import BaseCheckValueTest
from evidently.tests.base_test import TestValueCondition
from evidently.tests.utils import plot_check
from evidently.tests.utils import plot_metric_value
from evidently.tests.utils import regression_perf_plot
from evidently.tests.utils import plot_distr
from evidently.tests.utils import approx
from evidently.tests.utils import Numeric


class BaseRegressionPerformanceMetricsTest(BaseCheckValueTest, ABC):
    group = "regression"
    metric: RegressionPerformanceMetrics

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
        metric: Optional[RegressionPerformanceMetrics] = None,
    ):
        if metric is not None:
            self.metric = metric

        else:
            self.metric = RegressionPerformanceMetrics()

        super().__init__(eq=eq, gt=gt, gte=gte, is_in=is_in, lt=lt, lte=lte, not_eq=not_eq, not_in=not_in)


class TestValueMAE(BaseRegressionPerformanceMetricsTest):
    name = "Test MAE"

    def get_condition(self) -> TestValueCondition:
        if self.condition.is_set():
            return self.condition
        ref_mae = self.metric.get_result().mean_abs_error_ref
        if ref_mae is not None:
            return TestValueCondition(eq=approx(ref_mae, relative=0.1))
        return TestValueCondition(gt=self.metric.get_result().mean_abs_error_default)

    def calculate_value_for_test(self) -> Numeric:
        return self.metric.get_result().mean_abs_error

    def get_description(self, value: Numeric) -> str:
        return f"MAE value is {np.round(value, 3)} Threshold: [{self.get_condition()}]"


@default_renderer(test_type=TestValueMAE)
class TestValueMAERenderer(TestRenderer):
    def render_html(self, obj: TestValueMAE) -> TestHtmlInfo:
        info = super().render_html(obj)
        is_ref_data = False
        if "reference" in obj.metric.get_result().hist_for_plot.keys():
            is_ref_data = True
        fig = regression_perf_plot(
            val_for_plot=obj.metric.get_result().vals_for_plots["mean_abs_error"],
            hist_for_plot=obj.metric.get_result().hist_for_plot,
            name="MAE",
            curr_mertic=obj.metric.get_result().mean_abs_error,
            ref_metric=obj.metric.get_result().mean_abs_error_ref,
            is_ref_data=is_ref_data,
        )
        fig_json = fig.to_plotly_json()

        info.details.append(
            DetailsInfo(
                "MAE",
                "",
                BaseWidgetInfo(
                    title=fig_json["layout"]["title"]["text"],
                    size=2,
                    type="big_graph",
                    params={"data": fig_json["data"], "layout": fig_json["layout"]},
                ),
            )
        )
        return info


class TestValueMAPE(BaseRegressionPerformanceMetricsTest):
    name = "Test MAPE"

    def calculate_value_for_test(self) -> Numeric:
        return self.metric.get_result().mean_abs_perc_error

    def get_description(self, value: Numeric) -> str:
        return f"MAPE value is {np.round(value, 3)}"


@default_renderer(test_type=TestValueMAPE)
class TestValueMAPERenderer(TestRenderer):
    def render_html(self, obj: TestValueMAPE) -> TestHtmlInfo:
        info = super().render_html(obj)
        is_ref_data = False
        if "reference" in obj.metric.get_result().hist_for_plot.keys():
            is_ref_data = True
        fig = regression_perf_plot(
            val_for_plot=obj.metric.get_result().vals_for_plots["mean_abs_perc_error"],
            hist_for_plot=obj.metric.get_result().hist_for_plot,
            name="MAPE",
            curr_mertic=obj.metric.get_result().mean_abs_perc_error,
            ref_metric=obj.metric.get_result().mean_abs_perc_error_ref,
            is_ref_data=is_ref_data,
        )
        fig_json = fig.to_plotly_json()
        info.details.append(
            DetailsInfo(
                "MAPE",
                "",
                BaseWidgetInfo(
                    title=fig_json["layout"]["title"]["text"],
                    size=2,
                    type="big_graph",
                    params={"data": fig_json["data"], "layout": fig_json["layout"]},
                ),
            )
        )
        return info


class TestValueRMSE(BaseRegressionPerformanceMetricsTest):
    name = "Test RMSE"

    def calculate_value_for_test(self) -> Numeric:
        return self.metric.get_result().rmse

    def get_description(self, value: Numeric) -> str:
        return f"RMSE value is {np.round(value, 3)}"


@default_renderer(test_type=TestValueRMSE)
class TestValueRMSERenderer(TestRenderer):
    def render_html(self, obj: TestValueRMSE) -> TestHtmlInfo:
        info = super().render_html(obj)
        is_ref_data = False
        if "reference" in obj.metric.get_result().hist_for_plot.keys():
            is_ref_data = True
        fig = regression_perf_plot(
            val_for_plot=obj.metric.get_result().vals_for_plots["rmse"],
            hist_for_plot=obj.metric.get_result().hist_for_plot,
            name="RMSE",
            curr_mertic=obj.metric.get_result().rmse,
            ref_metric=obj.metric.get_result().rmse_ref,
            is_ref_data=is_ref_data,
        )
        fig_json = fig.to_plotly_json()
        info.details.append(
            DetailsInfo(
                "RMSE",
                "",
                BaseWidgetInfo(
                    title=fig_json["layout"]["title"]["text"],
                    size=2,
                    type="big_graph",
                    params={"data": fig_json["data"], "layout": fig_json["layout"]},
                ),
            )
        )
        return info


class TestValueMeanError(BaseRegressionPerformanceMetricsTest):
    name = "Test mean error"

    def calculate_value_for_test(self) -> Numeric:
        return self.metric.get_result().mean_error

    def get_description(self, value: Numeric) -> str:
        return f"Mean error value is {np.round(value, 3)}"


@default_renderer(test_type=TestValueMeanError)
class TestValueMeanErrorRenderer(TestRenderer):
    def render_html(self, obj: TestValueMeanError) -> TestHtmlInfo:
        info = super().render_html(obj)
        me_hist_for_plot = obj.metric.get_result().me_hist_for_plot
        hist_curr = me_hist_for_plot["current"]
        hist_ref = None
        if "reference" in obj.metric.get_result().me_hist_for_plot.keys():
            hist_ref = me_hist_for_plot["reference"]
        fig = plot_distr(hist_curr, hist_ref)
        fig = plot_check(fig, obj.condition)
        fig = plot_metric_value(fig, obj.metric.get_result().mean_error, "current mean error")

        fig_json = fig.to_plotly_json()
        info.details.append(
            DetailsInfo(
                id="",
                title="",
                info=BaseWidgetInfo(
                    title="",
                    size=2,
                    type="big_graph",
                    params={"data": fig_json["data"], "layout": fig_json["layout"]},
                ),
            )
        )
        return info


class TestValueAbsMaxError(BaseRegressionPerformanceMetricsTest):
    name = "Test Absolute Value of Max Error"

    def calculate_value_for_test(self) -> Numeric:
        return self.metric.get_result().abs_error_max

    def get_description(self, value: Numeric) -> str:
        return f"Absolute value of max error is {np.round(value, 3)}"


@default_renderer(test_type=TestValueAbsMaxError)
class TestValueAbsMaxErrorRenderer(TestRenderer):
    def render_html(self, obj: TestValueAbsMaxError) -> TestHtmlInfo:
        info = super().render_html(obj)
        me_hist_for_plot = obj.metric.get_result().me_hist_for_plot
        hist_curr = me_hist_for_plot["current"]
        hist_ref = None
        if "reference" in obj.metric.get_result().me_hist_for_plot.keys():
            hist_ref = me_hist_for_plot["reference"]
        fig = plot_distr(hist_curr, hist_ref)

        fig_json = fig.to_plotly_json()
        info.details.append(
            DetailsInfo(
                id="",
                title="",
                info=BaseWidgetInfo(
                    title="",
                    size=2,
                    type="big_graph",
                    params={"data": fig_json["data"], "layout": fig_json["layout"]},
                ),
            )
        )
        return info


class TestValueR2Score(BaseRegressionPerformanceMetricsTest):
    name = "Test R2 Score"

    def calculate_value_for_test(self) -> Numeric:
        return self.metric.get_result().r2_score

    def get_description(self, value: Numeric) -> str:
        return f"R2 score is {np.round(value, 3)}"


@default_renderer(test_type=TestValueR2Score)
class TestValueR2ScoreRenderer(TestRenderer):
    def render_html(self, obj: TestValueR2Score) -> TestHtmlInfo:
        info = super().render_html(obj)
        is_ref_data = False
        if "reference" in obj.metric.get_result().hist_for_plot.keys():
            is_ref_data = True
        fig = regression_perf_plot(
            val_for_plot=obj.metric.get_result().vals_for_plots["r2_score"],
            hist_for_plot=obj.metric.get_result().hist_for_plot,
            name="R2_score",
            curr_mertic=obj.metric.get_result().r2_score,
            ref_metric=obj.metric.get_result().r2_score_ref,
            is_ref_data=is_ref_data,
        )
        fig_json = fig.to_plotly_json()
        info.details.append(
            DetailsInfo(
                "R2_score",
                "",
                BaseWidgetInfo(
                    title="",
                    size=2,
                    type="big_graph",
                    params={"data": fig_json["data"], "layout": fig_json["layout"]},
                ),
            )
        )
        return info
