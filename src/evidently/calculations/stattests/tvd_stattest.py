from typing import Tuple

import numpy as np
import pandas as pd

from evidently.calculations.stattests.registry import StatTest
from evidently.calculations.stattests.registry import register_stattest
from evidently.calculations.stattests.utils import get_unique_not_nan_values_list_from_series
from evidently.calculations.stattests.utils import permutation_test


def _total_variation_distance(reference_data, current_data):
    """Compute the Total variation distance between two arrays
    Args:
        reference_data: reference data
        current_data: current data
    Returns:
        total_variation_distance: computed distance between reference_data and current_data
    """
    keys = get_unique_not_nan_values_list_from_series(current_data=current_data, reference_data=reference_data)
    ref_feature_dict = {**dict.fromkeys(keys, 0), **dict(reference_data.value_counts())}
    current_feature_dict = {**dict.fromkeys(keys, 0), **dict(current_data.value_counts())}
    ref = list(ref_feature_dict.values())
    curr = list(current_feature_dict.values())
    tvd = 0.5 * np.sum(np.abs(ref / sum(ref) - curr / sum(curr)))
    return tvd


def _tvd_stattest(
    reference_data: pd.Series,
    current_data: pd.Series,
    feature_type: str,
    threshold: float,
) -> Tuple[float, bool]:
    """Compute the Total variation distance (TVD) between two arrays
    Args:
        reference_data: reference data
        current_data: current data
        feature_type: feature type
        threshold: all values above this threshold means data drift
    Returns:
        p_value: two-sided p_value
        test_result: whether the drift is detected
    """

    observed = _total_variation_distance(reference_data, current_data)
    p_value = permutation_test(
        reference_data=reference_data,
        current_data=current_data,
        observed=observed,
        test_statistic_func=_total_variation_distance,
        iterations=1000,
    )

    return p_value, p_value < threshold


tvd_test = StatTest(
    name="TVD",
    display_name="Total-Variation-Distance",
    func=_tvd_stattest,
    allowed_feature_types=["cat"],
    default_threshold=0.1,
)

register_stattest(tvd_test)
