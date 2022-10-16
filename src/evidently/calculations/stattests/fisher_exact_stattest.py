from typing import Tuple

import numpy as np
import pandas as pd
from scipy.stats import fisher_exact

from evidently.calculations.stattests.registry import StatTest
from evidently.calculations.stattests.registry import register_stattest
from evidently.calculations.stattests.utils import get_unique_not_nan_values_list_from_series


def _fisher_test(
    reference_data: pd.Series, current_data: pd.Series, feature_type: str, threshold: float
) -> Tuple[float, bool]:
    """Calculate the p-value of Fisher's exact test between two arrays
    Args:
        reference_data: reference data
        current_data: current data
        feature_type: feature type
        threshold: all values above this threshold means data drift
    Returns:
        p_value: two-tailed p-value
        test_result: whether the drift is detected
    """

    contingency_matrix = pd.crosstab(reference_data, current_data)

    _, p_value = fisher_exact(contingency_matrix)

    return p_value, p_value < threshold


fisher_exact_test = StatTest(
    name="fisher",
    display_name="Fisher's Exact test",
    func=_fisher_test,
    allowed_feature_types=["cat"],
    default_threshold=0.1,
)

register_stattest(fisher_exact_test)
