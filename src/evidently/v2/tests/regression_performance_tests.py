from abc import ABC
from numbers import Number
from typing import List
from typing import Optional
from typing import Union

import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objs as go

from evidently.model.widget import BaseWidgetInfo
from evidently.options.color_scheme import RED, GREY
from evidently.v2.metrics import RegressionPerformanceMetrics
from evidently.v2.renderers.base_renderer import default_renderer, TestRenderer, TestHtmlInfo, DetailsInfo
from evidently.v2.tests.base_test import BaseCheckValueTest
from evidently.v2.tests.utils import plot_check, plot_metric_value, regression_perf_plot, plot_distr

class BaseRegressionPerformanceMetricsTest(BaseCheckValueTest, ABC):
    metric: RegressionPerformanceMetrics
    feature_name: str

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
            metric: Optional[RegressionPerformanceMetrics] = None
    ):
        if metric is not None:
            self.metric = metric

        else:
            self.metric = RegressionPerformanceMetrics()

        super().__init__(eq=eq, gt=gt, gte=gte, is_in=is_in, lt=lt, lte=lte, not_eq=not_eq, not_in=not_in)


class TestValueMAE(BaseRegressionPerformanceMetricsTest):
    name = "Test MAE"

    def calculate_value_for_test(self) -> Number:
        return self.metric.get_result().mean_abs_error

    def get_description(self, value: Number) -> str:
        return f"MAE value is {np.round(value, 3)}"


@default_renderer(test_type=TestValueMAE)
class TestValueMAERenderer(TestRenderer):
    def render_html(self, obj: TestValueMAE) -> TestHtmlInfo:
        info = super().render_html(obj)
        is_ref_data = False
        if 'reference' in obj.metric.get_result().hist_for_plot.keys():
            is_ref_data = True
        fig = regression_perf_plot(
            val_for_plot=obj.metric.get_result().vals_for_plots['mean_abs_error'],
            hist_for_plot=obj.metric.get_result().hist_for_plot,
            name='MAE', 
            curr_mertic=obj.metric.get_result().mean_abs_error, 
            ref_metric=obj.metric.get_result().mean_abs_error_ref, 
            is_ref_data=is_ref_data
        )
        fig_json = fig.to_plotly_json()
  
        info.details.append(
            DetailsInfo(
                'MAE',
                "",
                BaseWidgetInfo(
                    title=fig_json['layout']['title']['text'],
                    size=2,
                    type="big_graph",
                    params={"data": fig_json["data"], "layout": fig_json["layout"]},
                )
            )
        )
        return info


class TestValueMAPE(BaseRegressionPerformanceMetricsTest):
    name = "Test MAPE"

    def calculate_value_for_test(self) -> Number:
        return self.metric.get_result().mean_abs_perc_error

    def get_description(self, value: Number) -> str:
        return f"MAPE value is {np.round(value, 3)}"

@default_renderer(test_type=TestValueMAPE)
class TestValueMAPERenderer(TestRenderer):
    def render_html(self, obj: TestValueMAPE) -> TestHtmlInfo:
        info = super().render_html(obj)
        is_ref_data = False
        if 'reference' in obj.metric.get_result().hist_for_plot.keys():
            is_ref_data = True
        fig = regression_perf_plot(
            val_for_plot=obj.metric.get_result().vals_for_plots['mean_abs_perc_error'],
            hist_for_plot=obj.metric.get_result().hist_for_plot,
            name='MAPE',
            curr_mertic=obj.metric.get_result().mean_abs_perc_error,
            ref_metric=obj.metric.get_result().mean_abs_perc_error_ref,
            is_ref_data=is_ref_data
        )
        fig_json = fig.to_plotly_json()
        info.details.append(
            DetailsInfo(
                'MAPE',
                "",
                BaseWidgetInfo(
                    title=fig_json['layout']['title']['text'],
                    size=2,
                    type="big_graph",
                    params={"data": fig_json["data"], "layout": fig_json["layout"]},
                )
            )
        )
        return info


class TestValueRMSE(BaseRegressionPerformanceMetricsTest):
    name = "Test RMSE"

    def calculate_value_for_test(self) -> Number:
        return self.metric.get_result().rmse

    def get_description(self, value: Number) -> str:
        return f"RMSE value is {np.round(value, 3)}"


@default_renderer(test_type=TestValueRMSE)
class TestValueRMSERenderer(TestRenderer):
    def render_html(self, obj: TestValueRMSE) -> TestHtmlInfo:
        info = super().render_html(obj)
        is_ref_data = False
        if 'reference' in obj.metric.get_result().hist_for_plot.keys():
            is_ref_data = True
        fig = regression_perf_plot(
            val_for_plot=obj.metric.get_result().vals_for_plots['rmse'],
            hist_for_plot=obj.metric.get_result().hist_for_plot,
            name='RMSE', 
            curr_mertic=obj.metric.get_result().rmse, 
            ref_metric=obj.metric.get_result().rmse_ref, 
            is_ref_data=is_ref_data
        )
        fig_json = fig.to_plotly_json()
        info.details.append(
            DetailsInfo(
                'RMSE',
                "",
                BaseWidgetInfo(
                    title=fig_json['layout']['title']['text'],
                    size=2,
                    type="big_graph",
                    params={"data": fig_json["data"], "layout": fig_json["layout"]},
                )
            )
        )
        return info

class TestValueMeanError(BaseRegressionPerformanceMetricsTest):
    name = "Test mean error"

    def calculate_value_for_test(self) -> Number:
        return self.metric.get_result().mean_error

    def get_description(self, value: Number) -> str:
        return f"Mean error value is {np.round(value, 3)}"

@default_renderer(test_type=TestValueMeanError)
class TestValueMeanErrorRenderer(TestRenderer):
    def render_html(self, obj: TestValueMeanError) -> TestHtmlInfo:
        info = super().render_html(obj)
        me_hist_for_plot = obj.metric.get_result().me_hist_for_plot
        hist_curr = me_hist_for_plot['current']
        hist_ref = None
        if 'reference' in obj.metric.get_result().me_hist_for_plot.keys():
            hist_ref = me_hist_for_plot['reference']
        fig = plot_distr(hist_curr, hist_ref)
        fig = plot_check(fig, obj.condition)
        fig = plot_metric_value(fig, obj.metric.get_result().mean_error, 'current mean error')

        fig_json = fig.to_plotly_json()
        info.details.append(
            DetailsInfo(
                id="",
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


class TestValueAbsMaxError(BaseRegressionPerformanceMetricsTest):
    name = "Test Absolute Value of Max Error"

    def calculate_value_for_test(self) -> Number:
        return self.metric.get_result().abs_error_max

    def get_description(self, value: Number) -> str:
        return f"Absolute value of max error is {np.round(value, 3)}"

@default_renderer(test_type=TestValueAbsMaxError)
class TestValueAbsMaxErrorRenderer(TestRenderer):
    def render_html(self, obj: TestValueAbsMaxError) -> TestHtmlInfo:
        info = super().render_html(obj)
        me_hist_for_plot = obj.metric.get_result().me_hist_for_plot
        hist_curr = me_hist_for_plot['current']
        hist_ref = None
        if 'reference' in obj.metric.get_result().me_hist_for_plot.keys():
            hist_ref = me_hist_for_plot['reference']
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
                    params={"data": fig_json['data'], "layout": fig_json['layout']},
                )
            )
        )
        return info


class TestValueR2Score(BaseRegressionPerformanceMetricsTest):
    name = "Test R2 Score"

    def calculate_value_for_test(self) -> Number:
        return self.metric.get_result().r2_score

    def get_description(self, value: Number) -> str:
        return f"R2 score is {np.round(value, 3)}"

@default_renderer(test_type=TestValueR2Score)
class TestValueR2ScoreRenderer(TestRenderer):
    def render_html(self, obj: TestValueR2Score) -> TestHtmlInfo:
        info = super().render_html(obj)
        is_ref_data = False
        if 'reference' in obj.metric.get_result().hist_for_plot.keys():
            is_ref_data = True
        fig = regression_perf_plot(
            val_for_plot=obj.metric.get_result().vals_for_plots['r2_score'],
            hist_for_plot=obj.metric.get_result().hist_for_plot,
            name='R2_score', 
            curr_mertic=obj.metric.get_result().r2_score, 
            ref_metric=obj.metric.get_result().r2_score_ref, 
            is_ref_data=is_ref_data
        )
        fig_json = fig.to_plotly_json()
        info.details.append(
            DetailsInfo(
                'R2_score',
                "",
                BaseWidgetInfo(
                    title="",
                    size=2,
                    type="big_graph",
                    params={"data": fig_json["data"], "layout": fig_json["layout"]},
                )
            )
        )
        return info
