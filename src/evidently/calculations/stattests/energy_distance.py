"""Energy-distance test of two samples.

Name: "ed"

Import:

    >>> from evidently.calculations.stattests import energy_dist_test

Properties:
- only for numerical features
- returns p-value

Example:
    Using by object:

    >>> from evidently.options import DataDriftOptions
    >>> from evidently.calculations.stattests import energy_dist_test
    >>> options = DataDriftOptions(all_features_stattest=energy_dist_test)

    Using by name:

    >>> from evidently.options import DataDriftOptions
    >>> options = DataDriftOptions(all_features_stattest="ed")
"""
from typing import Tuple

import pandas as pd
from scipy.stats import energy_distance

from evidently.calculations.stattests.registry import StatTest
from evidently.calculations.stattests.registry import register_stattest


def _energy_dist(
    reference_data: pd.Series, current_data: pd.Series, feature_type: str, threshold: float
) -> Tuple[float, bool]:
    """Run the energy_distance test of two samples.
    Args:
        reference_data: reference data
        current_data: current data
        threshold: all values above this threshold propose a data drift
    Returns:
        distance: energy distance
        test_result: whether the drift is detected
    """
    distance = energy_distance(reference_data, current_data)
    return distance, distance > threshold


energy_dist_test = StatTest(
    name="ed", display_name="Energy-distance", func=_energy_dist, allowed_feature_types=["num"], default_threshold=0.1
)

register_stattest(energy_dist_test)
