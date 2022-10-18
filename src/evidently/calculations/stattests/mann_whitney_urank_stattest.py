from typing import Tuple

import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu

from evidently.calculations.stattests.registry import StatTest
from evidently.calculations.stattests.registry import register_stattest


def _mannwhitneyu_rank(
    reference_data: pd.Series, current_data: pd.Series, feature_type: str, threshold: float
) -> Tuple[float, bool]:
    """Perform the Mann-Whitney U-rank test between two arrays
    Args:
        reference_data: reference data
        current_data: current data
        feature_type: feature type
        threshold: all values above this threshold means data drift
    Returns:
        pvalue: the two-tailed p-value for the test depending on alternative and method
        test_result: whether the drift is detected
    """
    p_value = mannwhitneyu(x=reference_data, y=current_data)[1]
    return p_value, p_value < threshold


mann_whitney_u_stat_test = StatTest(
    name="mannw",
    display_name="Mann-Whitney U-rank test",
    func=_mannwhitneyu_rank,
    allowed_feature_types=["num"],
    default_threshold=0.05,
)

register_stattest(mann_whitney_u_stat_test)
