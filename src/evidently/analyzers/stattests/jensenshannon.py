from typing import Tuple

import pandas as pd
from scipy.spatial import distance

from evidently.analyzers.stattests.utils import get_binned_data

def jensenshannon(reference_data: pd.Series, current_data: pd.Series, threshold: float, n_bins: int = 30) -> Tuple[float, bool]:
    """Compute the Jensen-Shannon distance between two arrays
    Args:
            reference_data: reference data
            current_data: current data
            n_bins: number of bins
            threshold: all walues above this threshold means data drift
    Returns:
            jensenshannon: calculated Jensen-Shannon distance
            test_result: wether the drift is detected
    """
    # long_name Jensen-Shannon distance
    # short_name jensenshannon
    reference_percents, current_percents = get_binned_data(reference_data, current_data, n_bins)
    jensenshannon_value = distance.jensenshannon(reference_percents, current_percents)
    return jensenshannon_value, jensenshannon_value >= threshold