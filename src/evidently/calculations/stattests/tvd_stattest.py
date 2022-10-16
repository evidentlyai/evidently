from typing import Tuple

import numpy as np
import pandas as pd

from evidently.calculations.stattests.registry import StatTest
from evidently.calculations.stattests.registry import register_stattest


def _tvd_stattest(
    reference_data: pd.Series, current_data: pd.Series, feature_type: str, threshold: float, n_bins: int = 30
) -> Tuple[float, bool]:
    """Compute the Total variation distance (TVD) between two arrays
    Args:
        reference_data: reference data
        current_data: current data
        feature_type: feature type
        threshold: all values above this threshold means data drift
        n_bins: number of bins
    Returns:
        tvd: calculated Total variation distance value
        test_result: whether the drift is detected
    """
    ref = reference_data.values
    curr = current_data.values
    tvd = 0.5 * np.sum(np.abs(ref - curr))
    return tvd, tvd >= threshold


tvd_test = StatTest(
    name="tvd",
    display_name="Total-Variation-Distance",
    func=_tvd_stattest,
    allowed_feature_types=["num"],
    default_threshold=0.1,
)

register_stattest(tvd_test)
