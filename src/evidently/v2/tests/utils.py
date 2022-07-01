from typing import Dict

import numpy as np
import pandas as pd

import plotly.graph_objs as go
from plotly.subplots import make_subplots

RED = "#ed0400"
GREY = "#4d4d4d"


def plot_check(fig, condition):
    lines = []
    left_line = pd.Series([condition.gt, condition.gte]).max()
    if not pd.isnull(left_line):
        left_line_name = ['gt', 'gte'][pd.Series([condition.gt, condition.gte]).argmax()]
        lines.append((left_line, left_line_name))
    right_line = pd.Series([condition.lt, condition.lte]).min()
    if not pd.isnull(right_line):
        right_line_name = ['lt', 'lte'][pd.Series([condition.lt, condition.lte]).argmin()]
        lines.append((right_line, right_line_name))
    if condition.eq:
        lines.append((condition.eq, 'eq'))
    if condition.not_eq:
        lines.append((condition.not_eq, 'not_eq'))
    # if condition.ap:
    #     lines.append((condition.ap.value, 'ap'))

    fig = go.Figure(fig)
    max_y = np.max([np.max(x['y']) for x in fig.data])
    min_y = np.min([np.min(x['y']) for x in fig.data])
    if len(lines) > 0:
        for line, name in lines:
            fig.add_trace(go.Scatter(x=(line, line),
                                     y=(min_y, max_y),
                                     mode='lines',
                                     line=dict(color=GREY, width=3, dash='dash'),
                                     name=name))

    if left_line and right_line:
        fig.add_vrect(x0=left_line, x1=right_line, fillcolor='green', opacity=0.25, line_width=0)

    # if condition.ap:
    #     left_border=0
    #     right_border=0
    #     if condition.ap.rel:
    #         left_border =  condition.ap.value - condition.ap.value * condition.ap.rel
    #         right_border =  condition.ap.value + condition.ap.value * condition.ap.rel
    #     elif condition.ap.abs:
    #         left_border =  condition.ap.value - condition.ap.abs
    #         right_border =  condition.ap.value + condition.ap.abs
    #     fig.add_vrect(x0=left_border, x1=right_border, fillcolor='green', opacity=0.25, line_width=0)

    fig.update_layout(showlegend=True)

    return fig


def plot_metric_value(fig, metric_val: float, metric_name: str):
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


def plot_distr(hist_curr, hist_ref=None):
    fig = go.Figure()

    fig.add_trace(
        go.Bar(name='current', x=hist_curr['x'], y=hist_curr['count'], marker_color=RED)
    )
    if hist_ref is not None:
        fig.add_trace(
            go.Bar(name='reference', x=hist_ref['x'], y=hist_ref['count'], marker_color=GREY)
        )

    return fig


def regression_perf_plot(val_for_plot: Dict[str, pd.Series], hist_for_plot: Dict[str, pd.Series], name: str,
                         curr_mertic: float, ref_metric: float = None, is_ref_data: bool = False):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True)

    s = val_for_plot['current'].sort_index()
    x = [str(idx) for idx in s.index]
    y = [val for val in s]
    trace = go.Scatter(x=x, y=y, mode='lines+markers', name=name, marker_color=RED)
    fig.append_trace(trace, 1, 1)

    df = hist_for_plot['current'].sort_values('x')
    x = [str(x) for x in df.x]
    y = [val for val in df['count']]
    trace = go.Bar(name='current', x=x, y=y, marker_color=RED)
    fig.append_trace(trace, 2, 1)

    if is_ref_data:
        s = val_for_plot['reference'].sort_index()
        x = [str(idx) for idx in s.index]
        y = [val for val in s]
        trace = go.Scatter(x=x, y=y, mode='lines+markers', name=name, marker_color=GREY)
        fig.append_trace(trace, 1, 1)

        df = hist_for_plot['reference'].sort_values('x')
        x = [str(x) for x in df.x]
        y = [val for val in df['count']]
        trace = go.Bar(name='reference', x=x, y=y, marker_color=GREY)
        fig.append_trace(trace, 2, 1)
    fig.update_yaxes(title_text=name, row=1, col=1)
    fig.update_yaxes(title_text='count', row=2, col=1)
    title = f'current {name}: {np.round(curr_mertic, 3)} '
    if is_ref_data:
        title += f'<br>reference {name}: {np.round(ref_metric, 3)}'
    fig.update_layout(title=title)
    return fig
