from typing import Dict
from typing import Optional
from typing import Union

import numpy as np
import pandas as pd
from pandas.api.types import is_numeric_dtype

import plotly.graph_objs as go
from plotly.subplots import make_subplots

from evidently.model.widget import BaseWidgetInfo
from evidently.renderers.base_renderer import DetailsInfo


RED = "#ed0400"
GREY = "#4d4d4d"


# type for numeric because of mypy bug https://github.com/python/mypy/issues/3186
Numeric = Union[float, int]


def plot_check(fig, condition):
    lines = []
    left_line = pd.Series([condition.gt, condition.gte]).max()
    if not pd.isnull(left_line):
        left_line_name = ["gt", "gte"][pd.Series([condition.gt, condition.gte]).argmax()]
        lines.append((left_line, left_line_name))
    right_line = pd.Series([condition.lt, condition.lte]).min()
    if not pd.isnull(right_line):
        right_line_name = ["lt", "lte"][pd.Series([condition.lt, condition.lte]).argmin()]
        lines.append((right_line, right_line_name))
    if condition.eq and not isinstance(condition.eq, ApproxValue):
        lines.append((condition.eq, "eq"))
    if condition.eq and isinstance(condition.eq, ApproxValue):
        lines.append((condition.eq.value, "approx"))
    if condition.not_eq:
        lines.append((condition.not_eq, "not_eq"))

    fig = go.Figure(fig)
    max_y = np.max([np.max(x["y"]) for x in fig.data])
    min_y = np.min([np.min(x["y"]) for x in fig.data])
    if len(lines) > 0:
        for line, name in lines:
            fig.add_trace(
                go.Scatter(
                    x=(line, line),
                    y=(min_y, max_y),
                    mode="lines",
                    line=dict(color=GREY, width=3, dash="dash"),
                    name=name,
                )
            )

    if left_line and right_line:
        fig.add_vrect(x0=left_line, x1=right_line, fillcolor="green", opacity=0.25, line_width=0)

    if condition.eq and isinstance(condition.eq, ApproxValue):
        left_border = 0
        right_border = 0

        if condition.eq._relative > 1e-6:
            left_border = condition.eq.value - condition.eq.value * condition.eq._relative
            right_border = condition.eq.value + condition.eq.value * condition.eq._relative
            fig.add_vrect(x0=left_border, x1=right_border, fillcolor="green", opacity=0.25, line_width=0)
        elif condition.eq._absolute > 1e-12:
            left_border = condition.eq.value - condition.eq._absolute
            right_border = condition.eq.value + condition.eq._absolute
            fig.add_vrect(x0=left_border, x1=right_border, fillcolor="green", opacity=0.25, line_width=0)
        fig.add_vrect(x0=left_border, x1=right_border, fillcolor="green", opacity=0.25, line_width=0)

    fig.update_layout(showlegend=True)

    return fig


def plot_metric_value(fig, metric_val: float, metric_name: str):
    fig = go.Figure(fig)
    max_y = np.max([np.max(x["y"]) for x in fig.data])
    min_y = np.min([np.min(x["y"]) for x in fig.data])
    fig.add_trace(
        go.Scatter(
            x=(metric_val, metric_val),
            y=(min_y, max_y),
            mode="lines",
            line=dict(color="green", width=3),
            name=metric_name,
        )
    )
    fig.update_layout(showlegend=True)
    return fig


def plot_distr(hist_curr, hist_ref=None, orientation="v"):
    fig = go.Figure()

    fig.add_trace(
        go.Bar(name="current", x=hist_curr["x"], y=hist_curr["count"], marker_color=RED, orientation=orientation)
    )
    if hist_ref is not None:
        fig.add_trace(
            go.Bar(name="reference", x=hist_ref["x"], y=hist_ref["count"], marker_color=GREY, orientation=orientation)
        )

    return fig


def regression_perf_plot(
    val_for_plot: Dict[str, pd.Series],
    hist_for_plot: Dict[str, pd.Series],
    name: str,
    curr_mertic: float,
    ref_metric: float = None,
    is_ref_data: bool = False,
):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True)

    sorted_index = val_for_plot["current"].sort_index()
    x = [str(idx) for idx in sorted_index.index]
    y = list(sorted_index)
    trace = go.Scatter(x=x, y=y, mode="lines+markers", name=name, marker_color=RED)
    fig.append_trace(trace, 1, 1)

    df = hist_for_plot["current"].sort_values("x")
    x = [str(x) for x in df.x]
    y = list(df["count"])
    trace = go.Bar(name="current", x=x, y=y, marker_color=RED)
    fig.append_trace(trace, 2, 1)

    if is_ref_data:
        sorted_index = val_for_plot["reference"].sort_index()
        x = [str(idx) for idx in sorted_index.index]
        y = list(sorted_index)
        trace = go.Scatter(x=x, y=y, mode="lines+markers", name=name, marker_color=GREY)
        fig.append_trace(trace, 1, 1)

        df = hist_for_plot["reference"].sort_values("x")
        x = [str(x) for x in df.x]
        y = list(df["count"])
        trace = go.Bar(name="reference", x=x, y=y, marker_color=GREY)
        fig.append_trace(trace, 2, 1)

    fig.update_yaxes(title_text=name, row=1, col=1)
    fig.update_yaxes(title_text="count", row=2, col=1)
    title = f"current {name}: {np.round(curr_mertic, 3)} "

    if is_ref_data:
        title += f"<br>reference {name}: {np.round(ref_metric, 3)}"

    fig.update_layout(title=title)
    return fig


def plot_value_counts_tables(feature_name, values, curr_df, ref_df, id_prfx):
    additional_plots = []
    if values is not None:
        curr_df = curr_df[curr_df["count"] != 0]
        curr_vals_inside_lst = curr_df[curr_df.x.isin(values)].sort_values("count", ascending=False)
        if curr_vals_inside_lst.shape[0] > 0:
            additional_plots.append(
                DetailsInfo(
                    id=f"{id_prfx}_incide_{feature_name}",
                    title="Values inside the list (top 10)",
                    info=BaseWidgetInfo(
                        title="",
                        type="table",
                        params={"header": ["value", "count"], "data": curr_vals_inside_lst[:10].values},
                        size=2,
                    ),
                )
            )
        curr_vals_outside_lst = curr_df[~curr_df.x.isin(values)].sort_values("count", ascending=False)
        if curr_vals_outside_lst.shape[0] > 0:
            additional_plots.append(
                DetailsInfo(
                    id=f"{id_prfx}_outside_{feature_name}",
                    title="Values outside the list (top 10)",
                    info=BaseWidgetInfo(
                        title="",
                        type="table",
                        params={"header": ["value", "count"], "data": curr_vals_outside_lst[:10].values},
                        size=2,
                    ),
                )
            )
    elif ref_df is not None:
        curr_df = curr_df[curr_df["count"] != 0]
        ref_df = ref_df[ref_df["count"] != 0]

        if is_numeric_dtype(curr_df.x):
            new_values = np.setdiff1d(curr_df.x.values, ref_df.x.values)
            missed_values = np.setdiff1d(ref_df.x.values, curr_df.x.values)
        else:
            curr_df["x"] = curr_df["x"].astype(str)
            ref_df["x"] = ref_df["x"].astype(str)
            new_values = np.setdiff1d(curr_df.x.values, ref_df.x.values)
            missed_values = np.setdiff1d(ref_df.x.values, curr_df.x.values)
        new_values_data = curr_df[curr_df.x.isin(new_values)].sort_values("count", ascending=False)
        missed_values_data = ref_df[ref_df.x.isin(missed_values)].sort_values("count", ascending=False)
        additional_plots.append(
            DetailsInfo(
                id=f"{id_prfx}_new_{feature_name}",
                title="New values (top 10)",
                info=BaseWidgetInfo(
                    title="",
                    type="table",
                    params={"header": ["value", "count"], "data": new_values_data[:10].values},
                    size=2,
                ),
            )
        )
        additional_plots.append(
            DetailsInfo(
                id=f"{id_prfx}_missed_{feature_name}",
                title="Missing values (top 10)",
                info=BaseWidgetInfo(
                    title="",
                    type="table",
                    params={"header": ["value", "count"], "data": missed_values_data[:10].values},
                    size=2,
                ),
            )
        )

    return additional_plots


def plot_value_counts_tables_ref_curr(feature_name, curr_df, ref_df, id_prfx):
    additional_plots = []
    curr_df = curr_df[curr_df["count"] != 0]

    additional_plots.append(
        DetailsInfo(
            id=f"{id_prfx}_curr_{feature_name}",
            title="Current value counts (top 10)",
            info=BaseWidgetInfo(
                title="",
                type="table",
                params={"header": ["value", "count"], "data": curr_df[:10].values},
                size=2,
            ),
        )
    )
    if ref_df is not None:
        ref_df = ref_df[ref_df["count"] != 0]
        additional_plots.append(
            DetailsInfo(
                id=f"{id_prfx}_ref_{feature_name}",
                title="Reference value counts (top 10)",
                info=BaseWidgetInfo(
                    title="",
                    type="table",
                    params={"header": ["value", "count"], "data": ref_df[:10].values},
                    size=2,
                ),
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

    def __format__(self, format_spec):
        return f"{format(self.value, format_spec)} ± {format(self.tolerance, format_spec)}"

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

    def as_dict(self) -> dict:
        result = {"value": self.value}

        if self._relative is not None:
            result["relative"] = self._relative

        if self._absolute is not None:
            result["absolute"] = self._absolute

        return result


def approx(value, relative=None, absolute=None):
    """Get approximate value for checking a value is equal to other within some tolerance"""
    return ApproxValue(value=value, relative=relative, absolute=absolute)


def plot_dicts_to_table(
    dict_curr: dict, dict_ref: Optional[dict], columns: list, id_prfx: str, sort_by: str = "curr", asc: bool = False
):
    dict_for_df = {}
    dict_ref_keys = []
    if dict_ref is not None:
        dict_ref_keys = list(dict_ref.keys())
    keys = np.union1d(list(dict_curr.keys()), dict_ref_keys)
    dict_for_df[columns[0]] = keys
    dict_for_df[columns[1]] = [dict_curr.get(x, "NA") for x in keys]

    if dict_ref is not None:
        dict_for_df[columns[2]] = [dict_ref.get(x, "NA") for x in keys]
    df = pd.DataFrame(dict_for_df)
    if dict_ref is not None:
        if sort_by == "diff":
            df = df.astype(str)
            df["eq"] = (df[columns[1]] == df[columns[2]]).astype(int)
            df = df.sort_values("eq")
            df.drop("eq", axis=1, inplace=True)
    if sort_by == "curr":
        df_na = df[df[columns[1]] == "NA"]
        df_not_na = df[df[columns[1]] != "NA"]
        df_not_na = df_not_na.sort_values(columns[1], ascending=asc)
        df = pd.concat([df_na, df_not_na])
    df = df.astype(str)
    additional_plots = []
    additional_plots.append(
        DetailsInfo(
            id=id_prfx,
            title="",
            info=BaseWidgetInfo(
                title="",
                type="table",
                params={"header": list(df.columns), "data": df.values},
                size=2,
            ),
        )
    )

    return additional_plots


def plot_correlations(current_correlations, reference_correlations):
    columns = current_correlations.columns
    heatmap_text = None
    heatmap_texttemplate = None

    if reference_correlations is not None:
        cols = 2
        subplot_titles = ["current", "reference"]
    else:
        cols = 1
        subplot_titles = [""]

    fig = make_subplots(rows=1, cols=cols, subplot_titles=subplot_titles, shared_yaxes=True)
    if len(columns) < 15:
        heatmap_text = np.round(current_correlations, 2).astype(str)
        heatmap_texttemplate = "%{text}"

    trace = go.Heatmap(
        z=current_correlations,
        x=columns,
        y=columns,
        text=heatmap_text,
        texttemplate=heatmap_texttemplate,
        coloraxis="coloraxis",
    )
    fig.append_trace(trace, 1, 1)

    if reference_correlations is not None:
        if len(columns) < 15:
            heatmap_text = np.round(reference_correlations, 2).astype(str)
            heatmap_texttemplate = "%{text}"

        trace = go.Heatmap(
            z=reference_correlations,
            x=columns,
            y=columns,
            text=heatmap_text,
            texttemplate=heatmap_texttemplate,
            coloraxis="coloraxis",
        )
        fig.append_trace(trace, 1, 2)
    fig.update_layout(coloraxis={"colorscale": "RdBu_r"})
    return fig
