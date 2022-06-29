from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence
from typing import Union

import numpy as np
import pandas as pd

import plotly.graph_objs as go

from evidently.options import ColorOptions

RED = "#ed0400"
GREY = "#4d4d4d"

def plot_check(fig, gt=None, gte=None, lt=None, lte=None, ap=None, eq=None, not_eq=None):

    lines = []
    left_line = max(gt, gte)
    if left_line:
        left_line_name = ['gt', 'gte'][np.argmax(gt, gte)]
        lines.append((left_line, left_line_name))
    right_line = min(lt, lte)
    if right_line:
        right_line_name = ['lt', 'lte'][np.argmin(lt, lte)]
        lines.append((right_line, right_line_name))
    if eq:
        lines.append((eq, 'eq'))
    if not_eq:
        lines.append((not_eq, 'not_eq'))
    if ap:
        lines.append((ap.value, 'ap'))


    fig = go.Figure(fig)
    max_y = np.max([np.max(x['y']) for x in fig.data])
    min_y = np.min([np.min(x['y']) for x in fig.data])
    if len(lines) >0 :
        for line, name in lines:
            fig.add_trace(go.Scatter(x=(line, line),
                                    y=(min_y, max_y),
                                    mode='lines',
                                    line=dict(color=GREY, width=3, dash='dash'),
                                    name=name))

    if left_line and right_line:
        fig.add_vrect(x0=left_line, x1=right_line, fillcolor='green', opacity=0.25, line_width=0)

    if ap:
        left_border=0
        right_border=0
        if ap.rel:
            left_border =  ap.value - ap.value * ap.rel
            right_border =  ap.value + ap.value * ap.rel
        elif ap.abs:
            left_border =  ap.value - ap.abs
            right_border =  ap.value + ap.abs
        fig.add_vrect(x0=left_border, x1=right_border, fillcolor='green', opacity=0.25, line_width=0)

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
    fig= go.Figure()

    fig.add_trace(
        go.Bar(name='current', x=hist_curr['x'], y=hist_curr['count'], marker_color=RED)
        )
    if hist_ref is not None:
        fig.add_trace(
            go.Bar(name='reference', x=hist_ref['x'], y=hist_ref['count'], marker_color=GREY)
            )

    return fig


