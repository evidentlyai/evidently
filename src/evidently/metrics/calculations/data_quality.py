"""Methods for overall dataset quality calculations - rows count, a specific values count, etc."""

import pandas as pd


def get_rows_count(dataset: pd.DataFrame):
    """Count quantity of rows in  a dataset"""
    return dataset.shape[0]
