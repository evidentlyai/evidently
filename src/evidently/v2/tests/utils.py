from typing import Dict
from typing import Optional
from typing import Union

import numpy as np
import pandas as pd
from pandas.api.types import is_numeric_dtype

import plotly.graph_objs as go
from plotly.subplots import make_subplots

from evidently.model.widget import BaseWidgetInfo
from evidently.v2.renderers.base_renderer import DetailsInfo


RED = "#ed0400"
GREY = "#4d4d4d"


Numeric = Union[float, int]


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
            fig.add_trace(go.Scatter(
                x=(line, line),
                y=(min_y, max_y),
                mode='lines',
                line=dict(color=GREY, width=3, dash='dash'),
                name=name)
            )

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


def plot_distr(hist_curr, hist_ref=None, orientation='v'):
    fig = go.Figure()

    fig.add_trace(
        go.Bar(name='current', x=hist_curr['x'], y=hist_curr['count'], marker_color=RED, orientation=orientation)
    )
    if hist_ref is not None:
        fig.add_trace(
            go.Bar(name='reference', x=hist_ref['x'], y=hist_ref['count'], marker_color=GREY, orientation=orientation)
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


def plot_value_counts_tables(feature_name, values, curr_df, ref_df, id_prfx):
    additional_plots = []
    if values is not None:
        curr_df = curr_df[curr_df['count'] != 0]
        curr_vals_inside_lst = curr_df[curr_df.x.isin(values)].sort_values('count', ascending=False)
        if curr_vals_inside_lst.shape[0] > 0:
            additional_plots.append(
                DetailsInfo(
                    id=f"{id_prfx}_incide_{feature_name}",
                    title="Values inside the list (top 10)",
                    info=BaseWidgetInfo(
                        title="",
                        type="table",
                        params={
                            "header": ['value', 'count'],
                            "data": curr_vals_inside_lst[:10].values
                        },
                        size=2,
                    )
                )
            )
        curr_vals_outside_lst = curr_df[~curr_df.x.isin(values)].sort_values('count', ascending=False)
        if curr_vals_outside_lst.shape[0] > 0:
            additional_plots.append(
                DetailsInfo(
                    id=f"{id_prfx}_outside_{feature_name}",
                    title="Values outside the list (top 10)",
                    info=BaseWidgetInfo(
                        title="",
                        type="table",
                        params={
                            "header": ['value', 'count'],
                            "data": curr_vals_outside_lst[:10].values
                        },
                        size=2,
                    )
                )
            )
    elif ref_df is not None:
        curr_df = curr_df[curr_df['count'] != 0]
        ref_df = ref_df[ref_df['count'] != 0]

        if is_numeric_dtype(curr_df.x):
            new_values = np.setdiff1d(curr_df.x.values, ref_df.x.values)
            missed_values = np.setdiff1d(ref_df.x.values, curr_df.x.values)
        else:
            curr_df['x'] = curr_df['x'].astype(str)
            ref_df['x'] = ref_df['x'].astype(str)
            new_values = np.setdiff1d(curr_df.x.values, ref_df.x.values)
            missed_values = np.setdiff1d(ref_df.x.values, curr_df.x.values)
        new_values_data = curr_df[curr_df.x.isin(new_values)].sort_values('count', ascending=False)
        missed_values_data = ref_df[ref_df.x.isin(missed_values)].sort_values('count', ascending=False)
        additional_plots.append(
            DetailsInfo(
                id=f"{id_prfx}_new_{feature_name}",
                title="New values (top 10)",
                info=BaseWidgetInfo(
                    title="",
                    type="table",
                    params={
                        "header": ['value', 'count'],
                        "data": new_values_data[:10].values
                    },
                    size=2,
                )
            )
        )
        additional_plots.append(
            DetailsInfo(
                id=f"{id_prfx}_missed_{feature_name}",
                title="Missed values (top 10)",
                info=BaseWidgetInfo(
                    title="",
                    type="table",
                    params={
                        "header": ['value', 'count'],
                        "data": missed_values_data[:10].values
                    },
                    size=2,
                )
            )
        )

    return additional_plots


def plot_value_counts_tables_ref_curr(feature_name, curr_df, ref_df, id_prfx):
    additional_plots = []
    curr_df = curr_df[curr_df['count'] != 0]

    additional_plots.append(
        DetailsInfo(
            id=f"{id_prfx}_curr_{feature_name}",
            title="Current value counts (top 10)",
            info=BaseWidgetInfo(
                title="C",
                type="table",
                params={
                    "header": ['value', 'count'],
                    "data": curr_df[:10].values
                },
                size=2,
            )
        )
    )
    if ref_df is not None:
        ref_df = ref_df[ref_df['count'] != 0]
        additional_plots.append(
            DetailsInfo(
                id=f"{id_prfx}_ref_{feature_name}",
                title="Reference value counts (top 10)",
                info=BaseWidgetInfo(
                    title="",
                    type="table",
                    params={
                        "header": ['value', 'count'],
                        "data": ref_df[:10].values
                    },
                    size=2,
                )
            )
        )
    return additional_plots


class ApproxValue:
    """Class for approximate scalar value calculations"""
    DEFAULT_RELATIVE = 1e-6
    DEFAULT_ABSOLUTE = 1e-12
    value: Numeric
    _relative: Numeric
    _absolute: Numeric

    def __init__(self, value: Numeric, relative: Optional[Numeric] = None, absolute: Optional[Numeric] = None):
        self.value = value

        if relative is not None and relative <= 0:
            raise ValueError("Relative value for approx should be greater than 0")

        if relative is None:
            self._relative = self.DEFAULT_RELATIVE

        else:
            self._relative = relative

        if absolute is None:
            self._absolute = self.DEFAULT_ABSOLUTE

        else:
            self._absolute = absolute

    @property
    def tolerance(self) -> Numeric:
        relative_value = abs(self.value) * self._relative
        return max(relative_value, self._absolute)

    def __repr__(self):
        return f"{self.value} ± {self.tolerance}"

    def __eq__(self, other):
        tolerance = self.tolerance
        return (self.value - tolerance) <= other <= (self.value + tolerance)

    def __lt__(self, other):
        return self.value + self.tolerance < other

    def __le__(self, other):
        return self.value + self.tolerance <= other

    def __gt__(self, other):
        return self.value - self.tolerance > other

    def __ge__(self, other):
        return self.value - self.tolerance >= other


def approx(value, relative=None, absolute=None):
    """Get approximate value for checking a value is equal to other within some tolerance"""
    return ApproxValue(value=value, relative=relative, absolute=absolute)
