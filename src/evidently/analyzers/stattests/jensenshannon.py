from typing import Tuple

import pandas as pd
from scipy.spatial import distance

from evidently.analyzers.stattests.utils import get_binned_data
from evidently.analyzers.stattests.registry import StatTest, register_stattest


def _jensenshannon(
        reference_data: pd.Series,
        current_data: pd.Series,
        threshold: float,
        n_bins: int = 30) -> Tuple[float, bool]:
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
    reference_percents, current_percents = get_binned_data(reference_data, current_data, n_bins)
    jensenshannon_value = distance.jensenshannon(reference_percents, current_percents)
    return jensenshannon_value, jensenshannon_value >= threshold


jensenshannon_stat_test = StatTest(
    name="jensenshannon",
    display_name="Jensen-Shannon distance",
    func=_jensenshannon,
    allowed_feature_types=["num"]
)

register_stattest(jensenshannon_stat_test)
