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
    """Compute the first Wasserstein distance between two arrays normed by std of reference data
    Args:
        reference_data: reference data
        current_data: current data
        feature_type: feature type
        threshold: all values above this threshold means data drift
    Returns:
        wasserstein_distance_norm: normed Wasserstein distance
        test_result: whether the drift is detected
    """
    norm = max(np.std(reference_data), 0.001)
    wd_norm_value = stats.wasserstein_distance(reference_data, current_data) / norm
    return wd_norm_value, wd_norm_value >= threshold


wasserstein_stat_test = StatTest(
    name="wasserstein",
    display_name="Wasserstein distance (normed)",
    func=_wasserstein_distance_norm,
    allowed_feature_types=["num"],
    default_threshold=0.1,
)

register_stattest(wasserstein_stat_test)
