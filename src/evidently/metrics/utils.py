import pandas as pd
import sklearn.metrics

use_new_root_mean_squared_error = hasattr(sklearn.metrics, "root_mean_squared_error")


def root_mean_squared_error_compat(y_true, y_pred):
    """
    Compute the Root Mean Squared Error (RMSE) in a way that is compatible
    with both old and new versions of scikit-learn.

    In scikit-learn >= 1.6.0, uses sklearn.metrics.root_mean_squared_error.
    In earlier versions, uses mean_squared_error with squared=False.
    """
    if use_new_root_mean_squared_error:
        from sklearn.metrics import root_mean_squared_error

        return root_mean_squared_error(y_true, y_pred)

    from sklearn.metrics import mean_squared_error

    return mean_squared_error(y_true, y_pred, squared=False)


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
    df_for_bins["target_binned"] = pd.cut(df_for_bins[target_column], min(df_for_bins[target_column].nunique(), 10))
    return df_for_bins
