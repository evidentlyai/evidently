from typing import Tuple
import numpy as np
import pandas as pd


def make_hist_df(hist: Tuple[np.array, np.array]) -> pd.DataFrame:
    hist_df = pd.DataFrame(
        np.array([hist[1][:-1], hist[0], [f"{x[0]}-{x[1]}" for x in zip(hist[1][:-1], hist[1][1:])]]).T,
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


def make_hist_for_cat_plot(curr: pd.Series, ref: pd.Series = None):
    result = {}
    hist_df = curr.value_counts(dropna=False).reset_index()
    hist_df.columns = ["x", "count"]
    result["current"] = hist_df
    if ref is not None:
        hist_df = ref.value_counts().reset_index()
        hist_df.columns = ["x", "count"]
        result["reference"] = hist_df
    return result


def make_target_bins_for_reg_plots(
    curr: pd.DataFrame, target_column, preds_column, ref: pd.DataFrame = None
) -> pd.DataFrame:
    df_for_bins = pd.DataFrame({"data": "curr", target_column: curr[target_column], preds_column: curr[preds_column]})
    if ref is not None:
        df_for_bins = df_for_bins.append(
            pd.DataFrame({"data": "ref", target_column: ref[target_column], preds_column: ref[preds_column]})
        )
    df_for_bins["target_binned"] = pd.cut(df_for_bins[target_column], min(df_for_bins[target_column].nunique(), 10))
    return df_for_bins


def apply_func_to_binned_data(df_for_bins, func, target_column, preds_column, is_ref_data=False):
    result = {}
    result["current"] = (
        df_for_bins[df_for_bins.data == "curr"]
        .groupby("target_binned")
        .apply(lambda x: func(x[target_column], x[preds_column]))
    )

    if is_ref_data:
        result["reference"] = (
            df_for_bins[df_for_bins.data == "ref"]
            .groupby("target_binned")
            .apply(lambda x: func(x[target_column], x[preds_column]))
        )
    return result
