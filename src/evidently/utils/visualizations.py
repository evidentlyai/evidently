import json
from typing import Dict, Optional

import pandas as pd
import numpy as np

from plotly import graph_objs as go
from plotly.subplots import make_subplots

from evidently.options.color_scheme import ColorOptions


def plot_distr(hist_curr, hist_ref=None, orientation="v", color_options: Optional[ColorOptions] = None):
    color_options = color_options or ColorOptions()
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            name="current",
            x=hist_curr["x"],
            y=hist_curr["count"],
            marker_color=color_options.get_current_data_color(),
            orientation=orientation,
        )
    )
    if hist_ref is not None:
        fig.add_trace(
            go.Bar(
                name="reference",
                x=hist_ref["x"],
                y=hist_ref["count"],
                marker_color=color_options.get_reference_data_color(),
                orientation=orientation,
            )
        )
    if 'other' in hist_curr["x"] or (hist_ref is not None and 'other' in hist_ref["x"]):
        cats = list(fig.layout.xaxis.categoryarray)
        cats.remove("other")
        cats = cats + ["other"]
        fig.update_xaxes(categoryorder="array", categoryarray=cats)

    return fig


def plot_num_feature_in_time(curr_data: pd.DataFrame, ref_data: Optional[pd.DataFrame], feature_name: str,
                             datetime_name:str, freq: str):
    """
    Accepts current and reference data as pandas dataframes with two columns: datetime_name and feature_name. 
    """
    color_options = ColorOptions()
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=curr_data.sort_values(datetime_name)[datetime_name],
            y=curr_data.sort_values(datetime_name)[feature_name],
            line=dict(color=color_options.get_current_data_color(), shape="spline"),
            name="current",
        )
    )
    if ref_data is not None:
        fig.add_trace(
            go.Scatter(
                x=ref_data.sort_values(datetime_name)[datetime_name],
                y=ref_data.sort_values(datetime_name)[feature_name],
                line=dict(color=color_options.get_reference_data_color(), shape="spline"),
                name="reference",
            )
        )
        
        fig.update_layout(yaxis_title="Mean " + feature_name + " per " + freq)
        feature_in_time_figure = json.loads(fig.to_json())
    return feature_in_time_figure


def plot_time_feature_distr(curr_data: pd.DataFrame, ref_data: Optional[pd.DataFrame], feature_name: str):
    """
    Accepts current and reference data as pandas dataframes with two columns: feature_name, "number_of_items" 
    """
    color_options = ColorOptions()
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=curr_data.sort_values(feature_name)[feature_name],
            y=curr_data.sort_values(feature_name)["number_of_items"],
            line=dict(color=color_options.get_current_data_color(), shape="spline"),
            name="current",
        )
    )
    if ref_data is not None:
        fig.add_trace(
            go.Scatter(
                x=ref_data.sort_values(feature_name)[feature_name],
                y=ref_data.sort_values(feature_name)["number_of_items"],
                line=dict(color=color_options.get_reference_data_color(), shape="spline"),
                name="reference",
            )
        )
    # fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    fig = json.loads(fig.to_json())
    return fig


def plot_cat_feature_in_time(curr_data: pd.DataFrame, ref_data: Optional[pd.DataFrame], feature_name: str,
                             datetime_name:str, freq: str):
    """
    Accepts current and reference data as pandas dataframes with two columns: datetime_name and feature_name. 
    """
    color_options = ColorOptions()
    title = "current"
    fig = go.Figure()
    values = curr_data[feature_name].unique()
    if ref_data is not None:
        values = np.union1d(curr_data[feature_name].unique(), ref_data[feature_name].unique())
    for i, val in enumerate(values):
        fig.add_trace(
            go.Bar(
                x=curr_data.loc[curr_data[feature_name] == val, datetime_name],
                y=curr_data.loc[curr_data[feature_name] == val, "num"],
                name=str(val),
                marker_color=color_options.color_sequence[i],
                legendgroup=str(val)
            )
        )
        if ref_data is not None:
            title = "reference/current"
            fig.add_trace(
                go.Bar(
                    x=ref_data.loc[ref_data[feature_name] == val, datetime_name],
                    y=ref_data.loc[ref_data[feature_name] == val, "num"],
                    name=str(val),
                    marker_color=color_options.color_sequence[i],
                    # showlegend=False,
                    legendgroup=str(val),
                    opacity=0.6,
                )
            )
    fig.update_traces(marker_line_width=0.01)
    fig.update_layout(
        barmode="stack",
        bargap=0,
        yaxis_title="count category values per " + freq,
        title=title,
    )
    feature_in_time_figure = json.loads(fig.to_json())
    return feature_in_time_figure


def plot_boxes(curr_for_plots: dict, ref_for_plots: Optional[dict], yaxis_title: str, xaxis_title: str):
    """
    Accepts current and reference data as dicts with box parameters ("mins", "lowers", "uppers", "means", "maxs")
    and name of boxes parameter - "values"
    """
    color_options = ColorOptions()
    fig = go.Figure()
    trace = go.Box(
        lowerfence=curr_for_plots["mins"],
        q1=curr_for_plots["lowers"],
        q3=curr_for_plots["uppers"],
        median=curr_for_plots["means"],
        upperfence=curr_for_plots["maxs"],
        x=curr_for_plots["values"],
        name="current",
        marker_color=color_options.get_current_data_color(),
    )
    fig.add_trace(trace)
    if ref_for_plots is not None:
        trace = go.Box(
            lowerfence=curr_for_plots["mins"],
            q1=ref_for_plots["lowers"],
            q3=ref_for_plots["uppers"],
            median=ref_for_plots["means"],
            upperfence=ref_for_plots["maxs"],
            x=ref_for_plots["values"],
            name="reference",
            marker_color=color_options.get_reference_data_color(),
        )
        fig.add_trace(trace)
        fig.update_layout(boxmode="group")
    fig.update_layout(yaxis_title=yaxis_title, xaxis_title=xaxis_title, boxmode="group")
    fig = json.loads(fig.to_json())
    return fig

def plot_cat_cat_rel(curr: pd.DataFrame, ref: pd.DataFrame, target_name: str, feature_name: str):
    """
    Accepts current and reference data as pandas dataframes with two columns: feature_name and "count_objects". 
    """
    color_options = ColorOptions()
    cols = 1
    subplot_titles = ""
    if ref is not None:
        cols = 2
        subplot_titles = ["current", "reference"]
    fig = make_subplots(rows=1, cols=cols, shared_yaxes=True, subplot_titles=subplot_titles)
    for i, val in enumerate(curr[target_name].unique()):
        trace = go.Bar(
            x=curr.loc[curr[target_name] == val, feature_name],
            y=curr.loc[curr[target_name] == val, "count_objects"],
            marker_color=color_options.color_sequence[i],
            name=str(val),
            legendgroup=str(val)
            # showlegend=False,
        )
        fig.append_trace(trace, 1, 1)
    if ref is not None:
        for i, val in enumerate(ref[target_name].unique()):
            trace = go.Bar(
                x=ref.loc[ref[target_name] == val, feature_name],
                y=ref.loc[ref[target_name] == val, "count_objects"],
                marker_color=color_options.color_sequence[i],
                opacity=0.6,
                name=str(val),
                legendgroup=str(val)
            )
            fig.append_trace(trace, 1, 2)
    fig.update_layout(yaxis_title="count")
    fig = json.loads(fig.to_json())
    return fig

def plot_num_num_rel(curr: Dict[str, list], ref: Optional[Dict[str, list]], target_name: str, column_name: str):
    color_options = ColorOptions()
    cols = 1
    if ref is not None:
        cols = 2
    fig = make_subplots(rows=1, cols=cols, shared_yaxes=True)
    trace = go.Scatter(
        x=curr[column_name],
        y=curr[target_name],
        mode="markers",
        marker_color=color_options.get_current_data_color(),
        name="current",
    )
    fig.append_trace(trace, 1, 1)
    fig.update_xaxes(title_text=column_name, row=1, col=1)
    if ref is not None:
        trace = go.Scatter(
            x=ref[column_name],
            y=ref[target_name],
            mode="markers",
            marker_color=color_options.get_reference_data_color(),
            name="reference",
        )
        fig.append_trace(trace, 1, 2)
        fig.update_xaxes(title_text=column_name, row=1, col=2)
    fig.update_layout(yaxis_title=target_name, legend={"itemsizing": "constant"})
    fig.update_traces(marker_size=4)
    fig = json.loads(fig.to_json())
    return fig


# def plot_distr_with_log_button(hist_curr, hist_ref=None):
#     color_options = ColorOptions()

    # fig = go.Figure()
    # trace_1 = go.Bar(name="current", x=hist_curr["x"], y=hist_curr["count"], 
    #                  marker_color=color_options.get_current_data_color())

    # if current_data is None:
    #             trace1 = go.Histogram(x=reference_data[feature_name], marker_color=color_options.primary_color)
    #             trace2 = go.Histogram(
    #                 x=np.log10(reference_data.loc[reference_data[feature_name] > 0, feature_name]),
    #                 marker_color=color_options.primary_color,
    #                 visible=False,
    #             )
    #             data = [trace1, trace2]
    #             updatemenus = [
    #                 dict(
    #                     type="buttons",
    #                     direction="right",
    #                     x=1.0,
    #                     yanchor="top",
    #                     buttons=list(
    #                         [
    #                             dict(label="Linear Scale", method="update", args=[{"visible": [True, False]}]),
    #                             dict(label="Log Scale", method="update", args=[{"visible": [False, True]}]),
    #                         ]
    #                     ),
            #         )
            #     ]

            # else:
            #     trace1 = go.Histogram(
            #         x=reference_data[feature_name],
            #         marker_color=color_options.get_reference_data_color(),
            #         name="reference",
            #     )
            #     trace2 = go.Histogram(
            #         x=np.log10(reference_data.loc[reference_data[feature_name] > 0, feature_name]),
            #         marker_color=color_options.get_reference_data_color(),
            #         visible=False,
            #         name="reference",
            #     )
            #     trace3 = go.Histogram(
            #         x=current_data[feature_name], marker_color=color_options.get_current_data_color(), name="current"
            #     )
            #     trace4 = go.Histogram(
            #         x=np.log10(current_data.loc[current_data[feature_name] > 0, feature_name]),
            #         marker_color=color_options.get_current_data_color(),
            #         visible=False,
            #         name="current",
            #     )
            #     data = [trace1, trace2, trace3, trace4]

            #     updatemenus = [
            #         dict(
            #             type="buttons",
            #             direction="right",
            #             x=1.0,
            #             yanchor="top",
            #             buttons=list(
            #                 [
            #                     dict(
            #                         label="Linear Scale",
            #                         method="update",
            #                         args=[{"visible": [True, False, True, False]}],
            #                     ),
            #                     dict(
            #                         label="Log Scale", method="update", args=[{"visible": [False, True, False, True]}]
            #                     ),
            #                 ]
            #             ),
            #         )
            #     ]
            # layout = dict(updatemenus=updatemenus)

            # fig = go.Figure(data=data, layout=layout)
