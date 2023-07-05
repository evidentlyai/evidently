import numpy as np
import pandas as pd


def fixup_pandas_df_for_big_data(pandas_df: pd.DataFrame) -> pd.DataFrame:
    """convert *in-place* all str-like columns to np.str_"""
    for column in pandas_df.columns:
        if pandas_df[column].dtype == np.dtype("O"):
            pandas_df[column] = pandas_df[column].astype(np.str_)

    return pandas_df
