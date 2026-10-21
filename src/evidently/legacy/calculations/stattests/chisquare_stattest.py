"""Chisquare test of two samples.

Name: "chisquare"

Import:

    >>> from evidently.legacy.calculations.stattests import chi_stat_test

Properties:
- only for categorical features
- returns p-value

Example:
    Using by object:

    >>> from evidently.legacy.options.data_drift import DataDriftOptions
    >>> from evidently.legacy.calculations.stattests import chi_stat_test
    >>> options = DataDriftOptions(all_features_stattest=chi_stat_test)

    Using by name:

    >>> from evidently.legacy.options.data_drift import DataDriftOptions
    >>> options = DataDriftOptions(all_features_stattest="chisquare")
"""

from typing import Tuple

import pandas as pd
from scipy.stats import chi2_contingency

from evidently.legacy.calculations.stattests.registry import StatTest
from evidently.legacy.calculations.stattests.registry import register_stattest
from evidently.legacy.calculations.stattests.utils import get_unique_not_nan_values_list_from_series
from evidently.legacy.core import ColumnType


def _chi_stat_test(
    reference_data: pd.Series, current_data: pd.Series, feature_type: ColumnType, threshold: float
) -> Tuple[float, bool]:
    keys = get_unique_not_nan_values_list_from_series(current_data=current_data, reference_data=reference_data)
    ref_feature_dict = {**dict.fromkeys(keys, 0), **dict(reference_data.value_counts())}
    current_feature_dict = {**dict.fromkeys(keys, 0), **dict(current_data.value_counts())}
    # Both samples are drawn with sampling noise, so this is a two-sample test of homogeneity on the
    # 2 x k contingency table. Treating reference frequencies as known expected values ignores the
    # reference sampling variance and divides by zero for categories that only appear in current
    contingency_table = [[current_feature_dict[key] for key in keys], [ref_feature_dict[key] for key in keys]]
    p_value = chi2_contingency(contingency_table, correction=False)[1]
    return p_value, p_value < threshold


chi_stat_test = StatTest(
    name="chisquare",
    display_name="chi-square p_value",
    allowed_feature_types=[ColumnType.Categorical],
)

register_stattest(chi_stat_test, default_impl=_chi_stat_test)
