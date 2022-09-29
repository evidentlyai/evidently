from typing import Dict
from typing import Optional
from typing import Tuple

import numpy as np
import pandas as pd
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


def make_hist_for_num_plot(curr: pd.Series, ref: pd.Series = None):
    result = {}
    if ref is not None:
        ref = ref.dropna()
    bins = np.histogram_bin_edges(pd.concat([curr.dropna(), ref]), bins="doane")
    curr_hist = np.histogram(curr, bins=bins)
    result["current"] = make_hist_df(curr_hist)
    if ref is not None:
        ref_hist = np.histogram(ref, bins=bins)
        result["reference"] = make_hist_df(ref_hist)
    return result


def make_hist_for_cat_plot(curr: pd.Series, ref: pd.Series = None, normalize: bool = False):
    result = {}
    hist_df = curr.value_counts(normalize=normalize, dropna=False).reset_index()
    hist_df.columns = ["x", "count"]
    result["current"] = hist_df
    if ref is not None:
        hist_df = ref.value_counts(normalize=normalize).reset_index()
        hist_df.columns = ["x", "count"]
        result["reference"] = hist_df
    return result


def get_distribution_for_column(
    *, column_name: str, column_type: str, current_data: pd.DataFrame, reference_data: pd.DataFrame
) -> Dict[str, pd.DataFrame]:
    if column_type == "cat":
        return make_hist_for_cat_plot(current_data[column_name], reference_data[column_name])

    elif column_type == "num":
        return make_hist_for_num_plot(current_data[column_name], reference_data[column_name])

    else:
        raise ValueError(f"Cannot get distribution for column {column_name} with type {column_type}")


def make_hist_df(hist: Tuple[np.array, np.array]) -> pd.DataFrame:
    hist_df = pd.DataFrame(
        np.array([hist[1][:-1], hist[0], [f"{x[0]}-{x[1]}" for x in zip(hist[1][:-1], hist[1][1:])]]).T,
        columns=["x", "count", "range"],
    )

    hist_df["x"] = hist_df["x"].astype(float)
    hist_df["count"] = hist_df["count"].astype(int)
    return hist_df
