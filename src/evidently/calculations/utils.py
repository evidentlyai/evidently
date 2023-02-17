from typing import Tuple

import numpy as np
import pandas as pd


def make_hist_df(hist: Tuple[np.ndarray, np.ndarray]) -> pd.DataFrame:
    hist_df = pd.DataFrame(
        np.array(
            [
                hist[1][:-1],
                hist[0],
                [f"{x[0]}-{x[1]}" for x in zip(hist[1][:-1], hist[1][1:])],
            ]
        ).T,
        columns=["x", "count", "range"],
    )

    hist_df["x"] = hist_df["x"].astype(float)
    hist_df["count"] = hist_df["count"].astype(int)
    return hist_df


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


def make_hist_for_cat_plot(curr: pd.Series, ref: pd.Series = None, normalize: bool = False, dropna=False):
    result = {}
    hist_df = curr.astype(str).value_counts(normalize=normalize, dropna=dropna).reset_index()
    hist_df.columns = ["x", "count"]
    result["current"] = hist_df
    if ref is not None:
        hist_df = ref.astype(str).value_counts(normalize=normalize, dropna=dropna).reset_index()
        hist_df.columns = ["x", "count"]
        result["reference"] = hist_df
    return result
