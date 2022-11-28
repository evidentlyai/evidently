"""Kolmogorov-Smirnov test of two samples.

Name: "ks"

Import:

    >>> from evidently.calculations.stattests import ks_stat_test

Properties:
- only for numerical features
- returns p-value

Example:
    Using by object:

    >>> from evidently.options import DataDriftOptions
    >>> from evidently.calculations.stattests import ks_stat_test
    >>> options = DataDriftOptions(all_features_stattest=ks_stat_test)

    Using by name:

    >>> from evidently.options import DataDriftOptions
    >>> options = DataDriftOptions(all_features_stattest="ks")
"""
from typing import Tuple

import pandas as pd
from scipy.stats import ks_2samp

from evidently.calculations.stattests.registry import StatTest
from evidently.calculations.stattests.registry import register_stattest


def _ks_stat_test(
    reference_data: pd.Series, current_data: pd.Series, feature_type: str, threshold: float
) -> Tuple[float, bool]:
    """Run the two-sample Kolmogorov-Smirnov test of two samples. Alternative: two-sided
    Args:
        reference_data: reference data
        current_data: current data
        feature_type: feature type
        threshold: level of significance
    Returns:
        p_value: two-tailed p-value
        test_result: whether the drift is detected
    """
    p_value = ks_2samp(reference_data, current_data)[1]
    return p_value, p_value <= threshold


ks_stat_test = StatTest(
    name="ks", display_name="K-S p_value", func=_ks_stat_test, allowed_feature_types=["num"], default_threshold=0.05
)

register_stattest(ks_stat_test)
