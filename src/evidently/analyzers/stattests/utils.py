import pandas as pd
import numpy as np


def get_binned_data(reference: pd.Series, current: pd.Series, n: int):
    """Split variable into n buckets based on reference quantiles
    Args:
      reference: reference data
      current: current data
      n: number of quantiles
    Returns:
      reference_percents: % of records in each bucket for reference
      current_percents: % of records in each bucket for reference
    """

    _, bins = pd.qcut(reference, n, retbins=True)

    reference_percents = np.histogram(reference, bins)[0] / len(reference)
    current_percents = np.histogram(current, bins)[0] / len(current)

    np.place(reference_percents, reference_percents == 0, 0.0001)
    np.place(current_percents, current_percents == 0, 0.0001)

    return reference_percents, current_percents
