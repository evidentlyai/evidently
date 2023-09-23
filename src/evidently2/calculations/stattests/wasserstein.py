from typing import Tuple

import numpy as np
import pandas as pd
from scipy import stats

from evidently2.calculations.basic import Div, Max, MoreThen, Std
from evidently2.calculations.stattests.base import StatTest
from evidently2.core.calculation import Calculation, Constant, _CalculationBase


class Wasserstein(Calculation):
    current: _CalculationBase


def _wasserstein_distance_norm(
    reference_data: Calculation, current_data: Calculation, feature_type: str, threshold: float
) -> Tuple[Calculation, Calculation]:
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
    # norm = max(np.std(reference_data), 0.001)
    # wd_norm_value = stats.wasserstein_distance(reference_data, current_data) / norm
    norm = Max(input_data=Std(input_data=reference_data), second=Constant(0.001))

    wd_norm_value = Div(input_data=Wasserstein(input_data=reference_data, current=current_data), second=norm)
    return wd_norm_value, MoreThen(input_data=wd_norm_value, second=Constant(threshold), equal=True) # wd_norm_value >= threshold


wasserstein_stat_test = StatTest(
    name="wasserstein",
    display_name="Wasserstein distance (normed)",
    func=_wasserstein_distance_norm,
    allowed_feature_types=["num"],
    default_threshold=0.1,
)

