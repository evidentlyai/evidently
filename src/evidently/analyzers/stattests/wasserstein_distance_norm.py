from typing import Tuple

import pandas as pd
import numpy as np
from scipy import stats

from evidently.analyzers.stattests.registry import StatTest, register_stattest


def _wasserstein_distance_norm(
        reference_data: pd.Series,
        current_data: pd.Series,
        feature_type: str,
        threshold: float) -> Tuple[float, bool]:
    """Compute the first Wasserstein distance between two arrays normed by mean value of reference data
    Args:
        reference_data: reference data
        current_data: current data
        feature_type: feature type
        threshold: all walues above this threshold means data drift
    Returns:
        wasserstein_distance_norm: normed Wasserstein distance
        test_result: wether the drift is detected
    """
    norm = np.mean(reference_data) if np.mean(reference_data) != 0 else 0.0001
    wd_norm_value = stats.wasserstein_distance(reference_data, current_data) / np.abs(norm)
    return wd_norm_value, wd_norm_value >= threshold


wasserstein_stat_test = StatTest(
    name="wasserstein",
    display_name="Wasserstein distance (normed)",
    func=_wasserstein_distance_norm,
    allowed_feature_types=["num"]
)

register_stattest(wasserstein_stat_test)
