from typing import Tuple

import pandas as pd
import numpy as np
from scipy import stats


def wasserstein_distance_norm(reference_data: pd.Series, current_data: pd.Series, threshold: float) -> Tuple[float, bool]:
    """Compute the first Wasserstein distance between two arrays normed by mean value of reference data
    Args:
        reference_data: reference data
        current_data: current data
        threshold: all walues above this threshold means data drift
    Returns:
        wasserstein_distance_norm: normed Wasserstein distance
        test_result: wether the drift is detected
    """
    # long_name wasserstein_distance_normed
    # short_name wasserstein_distance_normed
    norm = np.mean(reference_data) if np.mean(reference_data) != 0 else 0.0001
    wd_norm_value = stats.wasserstein_distance(reference_data, current_data) / np.abs(norm)
    return wd_norm_value, wd_norm_value >= threshold
