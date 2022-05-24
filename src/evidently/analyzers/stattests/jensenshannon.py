from typing import Tuple

import pandas as pd
from scipy.spatial import distance

from evidently.analyzers.stattests.utils import get_binned_data
from evidently.analyzers.stattests.registry import StatTest, register_stattest


def _jensenshannon(
        reference_data: pd.Series,
        current_data: pd.Series,
        feature_type: str,
        threshold: float,
        n_bins: int = 30) -> Tuple[float, bool]:
    """Compute the Jensen-Shannon distance between two arrays
    Args:
        reference_data: reference data
        current_data: current data
        feature_type: feature type
        threshold: all values above this threshold means data drift
        n_bins: number of bins
    Returns:
        jensenshannon: calculated Jensen-Shannon distance
        test_result: whether the drift is detected
    """
    reference_percents, current_percents = get_binned_data(reference_data, current_data, feature_type, n_bins, False)
    jensenshannon_value = distance.jensenshannon(reference_percents, current_percents)
    return jensenshannon_value, jensenshannon_value >= threshold


jensenshannon_stat_test = StatTest(
    name="jensenshannon",
    display_name="Jensen-Shannon distance",
    func=_jensenshannon,
    allowed_feature_types=["cat", "num"],
    default_threshold=0.1,
)

register_stattest(jensenshannon_stat_test)
