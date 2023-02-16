"""Anderson-Darling test of two samples.

Name: "anderson"

Import:

    >>> from evidently.calculations.stattests import anderson_darling_test

Properties:
- only for numerical features
- returns p-value

Example:
    Using by object:

    >>> from evidently.options import DataDriftOptions
    >>> from evidently.calculations.stattests import anderson_darling_test
    >>> options = DataDriftOptions(all_features_stattest=anderson_darling_test)

    Using by name:

    >>> from evidently.options import DataDriftOptions
    >>> options = DataDriftOptions(all_features_stattest="anderson")
"""
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
    p_value = anderson_ksamp([reference_data.values, current_data.values])[2]
    return p_value, p_value < threshold


anderson_darling_test = StatTest(
    name="anderson",
    display_name="Anderson-Darling",
    func=_anderson_darling,
    allowed_feature_types=["num"],
    default_threshold=0.1,
)

register_stattest(anderson_darling_test)
