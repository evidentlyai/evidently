from typing import Tuple

import pandas as pd
from scipy import stats

from evidently.analyzers.stattests.utils import get_binned_data

def kl_div(reference_data: pd.Series, current_data: pd.Series, threshold: float, n_bins: int = 30) -> Tuple[float, bool]:
    """Compute the Kullback-Leibler divergence between two arrays
    Args:
        reference_data: reference data
        current_data: current data
        n_bins: number of bins
        threshold: all walues above this threshold means data drift
    Returns:
        kl_div: calculated Kullback-Leibler divergence value
        test_result: wether the drift is detected
    """
    # long_name Kullback-Leibler divergence
    # short_name kl_div
    reference_percents, current_percents = get_binned_data(reference_data, current_data, n_bins)
    kl_div_value = stats.entropy(reference_percents, current_percents)
    return kl_div_value, kl_div_value >= threshold
