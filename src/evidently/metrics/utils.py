import pandas as pd


def make_target_bins_for_reg_plots(
    curr: pd.DataFrame, target_column, preds_column, ref: pd.DataFrame = None
) -> pd.DataFrame:
    df_for_bins = pd.DataFrame(
        {
            "data": "curr",
            target_column: curr[target_column],
            preds_column: curr[preds_column],
        }
    )
    if ref is not None:
        df_for_bins = pd.concat(
            [
                df_for_bins,
                pd.DataFrame(
                    {
                        "data": "ref",
                        target_column: ref[target_column],
                        preds_column: ref[preds_column],
                    }
                ),
            ]
        )
    df_for_bins["target_binned"] = pd.cut(
        df_for_bins[target_column], min(df_for_bins[target_column].nunique(), 10)
    )
    return df_for_bins


def apply_func_to_binned_data(
    df_for_bins, func, target_column, preds_column, is_ref_data=False
):
    result = {}

    def _apply(x):
        if x.shape[0] == 0:
            return None
        return func(x[target_column], x[preds_column])

    result["current"] = (
        df_for_bins[df_for_bins.data == "curr"].groupby("target_binned").apply(_apply)
    )

    if is_ref_data:
        result["reference"] = (
            df_for_bins[df_for_bins.data == "ref"]
            .groupby("target_binned")
            .apply(_apply)
        )
    return result
