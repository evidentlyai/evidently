import json
from typing import Optional

import pandas as pd
import numpy as np

from plotly import graph_objs as go

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

import logging
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
    logging.warning(values)
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
