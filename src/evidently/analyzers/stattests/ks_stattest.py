#!/usr/bin/env python
# coding: utf-8
from typing import Tuple

import pandas as pd
from scipy.stats import ks_2samp


def ks_stat_test(reference_data: pd.Series, current_data: pd.Series, threshold: float) -> Tuple[float, bool]:
    """Run the two-sample Kolmogorov-Smirnov test of two samples. Alternative: two-sided
    Args:
        reference_data: reference data
        current_data: current data
        threshold: level of significance
    Returns:
        p_value: two-tailed p-value
        test_result: wether the drift is detected
    """
    # long_name ks_stat_test p_value
    # short_name ks_stat_test
    p_value = ks_2samp(reference_data, current_data)[1]
    return p_value, p_value <= threshold
