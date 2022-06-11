from typing import Tuple

import pandas as pd
import numpy as np

from evidently.analyzers.stattests.registry import StatTest, register_stattest
from evidently.analyzers.stattests.utils import get_binned_data


def psi(
        reference_data: pd.Series,
        current_data: pd.Series,
        feature_type: str,
        threshold: float,
        n_bins: int = 30) -> Tuple[float, bool]:
    """Calculate the PSI
    Args:
        reference_data: reference data
        current_data: current data
        feature_type: feature type
        threshold: all values above this threshold means data drift
        n_bins: number of bins
    Returns:
        psi_value: calculated PSI
        test_result: whether the drift is detected
    """
    reference_percents, current_percents = get_binned_data(reference_data, current_data, feature_type, n_bins)

    def sub_psi(ref_perc, curr_perc):
        """Calculate the actual PSI value from comparing the values.
            Update the actual value to a very small number if equal to zero
        """
        value = (ref_perc - curr_perc) * np.log(ref_perc / curr_perc)
        return value

    psi_value = 0
    for i, _ in enumerate(reference_percents):
        psi_value += sub_psi(reference_percents[i], current_percents[i])

    return psi_value, psi_value >= threshold


psi_stat_test = StatTest(
    name="psi",
    display_name="PSI",
    func=psi,
    allowed_feature_types=["cat", "num"],
    default_threshold=0.1,
)

register_stattest(psi_stat_test)
