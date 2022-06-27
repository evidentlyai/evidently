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
        return f"MAE value is {value}"


@default_renderer(test_type=TestValueMAE)
class TestValueMAERenderer(TestRenderer):
    def render_html(self, obj: TestValueMAE) -> TestHtmlInfo:
        info = super().render_html(obj)
        mae_distr = obj.metric.get_result().mae_distr
        ref_mae_distr = obj.metric.get_result().ref_mae_distr
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True)
        trace = go.Scatter(x=[str(idx) for idx, _, _ in mae_distr], y=[mae for _, mae, _ in mae_distr],
                           mode='lines+markers',
                           name='MAE', marker_color=RED)
        fig.append_trace(trace, 1, 1)
        if ref_mae_distr:
            trace_ref = go.Scatter(x=[str(idx) for idx, _, _ in mae_distr], y=[mae for _, mae, _ in ref_mae_distr],
                                   mode='lines+markers',
                                   name='MAE', marker_color=GREY)
            fig.append_trace(trace_ref, 1, 1)

        trace = go.Bar(name='current', x=[str(idx) for idx, _, _ in mae_distr], y=[hist for _, _, hist in mae_distr],
                       marker_color=RED)
        if ref_mae_distr:
            trace_ref = go.Bar(name='current',
                               x=[str(idx) for idx, _, _ in ref_mae_distr],
                               y=[hist for _, _, hist in ref_mae_distr],
                               marker_color=GREY)
            fig.append_trace(trace_ref, 2, 1)
        fig.append_trace(trace, 2, 1)
        fig.update_yaxes(title_text='MAE', row=1, col=1)
        fig.update_yaxes(title_text='count', row=2, col=1)
        fig.update_layout(title=f'MAE: {np.round(obj.metric.get_result().mean_abs_error, 3)}')
        fig_json = fig.to_plotly_json()
        info.details.append(
            DetailsInfo(
                "",
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


class TestValueMAPE(BaseRegressionPerformanceMetricsTest):
    name = "Test MAPE"

    def calculate_value_for_test(self) -> Number:
        return self.metric.get_result().mean_abs_perc_error

    def get_description(self, value: Number) -> str:
        return f"MAPE value is {value}"


class TestValueRMSE(BaseRegressionPerformanceMetricsTest):
    name = "Test RMSE"

    def calculate_value_for_test(self) -> Number:
        return self.metric.get_result().rmsa

    def get_description(self, value: Number) -> str:
        return f"RMSE value is {value}"


class TestValueMeanError(BaseRegressionPerformanceMetricsTest):
    name = "Test mean error"

    def calculate_value_for_test(self) -> Number:
        return self.metric.get_result().mean_error

    def get_description(self, value: Number) -> str:
        return f"Mean error value is {value}"


class TestValueAbsMaxError(BaseRegressionPerformanceMetricsTest):
    name = "Test Absolute Value of Max Error"

    def calculate_value_for_test(self) -> Number:
        return self.metric.get_result().abs_error_max

    def get_description(self, value: Number) -> str:
        return f"Absolute value of max error is {value}"


class TestValueR2Score(BaseRegressionPerformanceMetricsTest):
    name = "Test R2 Score"

    def calculate_value_for_test(self) -> Number:
        return self.metric.get_result().r2_score

    def get_description(self, value: Number) -> str:
        return f"R2 score is {value}"


@default_renderer(test_type=TestValueMeanError)
class TestValueMeanErrorRenderer(TestRenderer):
    def render_html(self, obj: TestValueMeanError) -> TestHtmlInfo:
        info = super().render_html(obj)
        me_distr = obj.metric.get_result().me_distr
        ref_me_distr = obj.metric.get_result().ref_me_distr
        cur_bar = go.Bar(name='current', x=[x for x, _ in me_distr], y=[y for _, y in me_distr], marker_color=RED)
        if ref_me_distr is None:
            fig = go.Figure(data=[
                go.Bar(name='current', x=[x for x, _ in me_distr], y=[y for _, y in me_distr], marker_color=RED)
            ])
            fig = plot_check(fig, gt=-0.05, lt=0.05)
            fig = plot_metric_value(fig, obj.metric.get_result().mean_error, 'ME')
        else:
            ref_bar = go.Bar(name='reference',
                             x=[x for x, _ in ref_me_distr],
                             y=[y for _, y in ref_me_distr],
                             marker_color=GREY)
            fig = make_subplots(rows=1, cols=2, shared_yaxes=True)
            fig.append_trace(ref_bar, 1, 1)
            fig.append_trace(cur_bar, 1, 2)
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


def plot_check(fig, gt=None, lt=None, the_approx=None, the_exact=None):
    fig = go.Figure(fig)
    max_y = np.max([np.max(x['y']) for x in fig.data])
    min_y = np.min([np.min(x['y']) for x in fig.data])
    if gt:
        fig.add_trace(go.Scatter(x=(gt, gt),
                                 y=(min_y, max_y),
                                 mode='lines',
                                 line=dict(color=GREY, width=3, dash='dash'),
                                 name='gt'))
    if lt:
        fig.add_trace(go.Scatter(x=(lt, lt),
                                 y=(min_y, max_y),
                                 mode='lines',
                                 line=dict(color=GREY, width=3, dash='dash'),
                                 name='lt'))
    if the_exact:
        fig.add_trace(go.Scatter(x=(the_exact, the_exact),
                                 y=(min_y, max_y),
                                 mode='lines',
                                 line=dict(color=GREY, width=3, dash='dash'),
                                 name='the_exact'))
    if gt and lt:
        fig.add_vrect(x0=gt, x1=lt, fillcolor='green', opacity=0.25, line_width=0)
    if the_approx:
        fig.add_trace(go.Scatter(x=(the_approx[0], the_approx[0]),
                                 y=(min_y, max_y),
                                 mode='lines',
                                 line=dict(color=GREY, width=3, dash='dash'),
                                 name='the_approx'))
        fig.add_vrect(x0=the_approx[0] - the_approx[0] * the_approx[1],
                      x1=the_approx[0] + the_approx[0] * the_approx[1], fillcolor='green', opacity=0.25, line_width=0)
    fig.update_layout(showlegend=True)
    return fig


def plot_metric_value(fig, metric_val, metric_name):
    fig = go.Figure(fig)
    max_y = np.max([np.max(x['y']) for x in fig.data])
    min_y = np.min([np.min(x['y']) for x in fig.data])
    fig.add_trace(go.Scatter(x=(metric_val, metric_val),
                             y=(min_y, max_y),
                             mode='lines',
                             line=dict(color='green', width=3),
                             name=metric_name))
    fig.update_layout(showlegend=True)
    return fig
