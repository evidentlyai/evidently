from typing import Tuple

import numpy as np
import pandas as pd
from scipy.stats import anderson_ksamp

from evidently.calculations.stattests.registry import StatTest
from evidently.calculations.stattests.registry import register_stattest


def _anderson_darling(
    reference_data: pd.Series,
    current_data: pd.Series,
    feature_type: str,
    threshold: float,
) -> Tuple[float, bool]:
    """Run the  Anderson-Darling test of two samples.
    Args:
        reference_data: reference data
        current_data: current data
        feature_type: feature type
        threshold: level of significance
    Returns:
        p_value: p-value
        test_result: whether the drift is detected
    """
    p_value = anderson_ksamp(np.array([reference_data, current_data]))[2]
    return p_value, p_value < threshold


anderson_darling_test = StatTest(
    name="anderson",
    display_name="Anderson-Darling",
    func=_anderson_darling,
    allowed_feature_types=["num"],
    default_threshold=0.1,
)

register_stattest(anderson_darling_test)
