"""Anderson-Darling test of two samples.

Name: "anderson"

Import:

    >>> from evidently.legacy.calculations.stattests import anderson_darling_test

Properties:
- only for numerical features
- returns p-value

Example:
    Using by object:

    >>> from evidently.legacy.options.data_drift import DataDriftOptions
    >>> from evidently.legacy.calculations.stattests import anderson_darling_test
    >>> options = DataDriftOptions(all_features_stattest=anderson_darling_test)

    Using by name:

    >>> from evidently.legacy.options.data_drift import DataDriftOptions
    >>> options = DataDriftOptions(all_features_stattest="anderson")
"""

from typing import Tuple

import pandas as pd
import scipy
from scipy.stats import anderson_ksamp

from evidently.legacy.calculations.stattests.registry import StatTest
from evidently.legacy.calculations.stattests.registry import register_stattest
from evidently.legacy.core import ColumnType

# scipy>=1.17 deprecates the `midrank` keyword in favour of `variant=`. When
# `variant` is supplied the return object is no longer a 3-tuple and exposes
# `pvalue` instead. Use the new API on scipy>=1.17 to silence the
# DeprecationWarning reported in issue #1534, and fall back to the legacy
# tuple shape on older scipy. The minimum supported scipy is 1.10 per
# pyproject.toml, so the fallback path is required.
_SCIPY_VERSION: Tuple[int, ...] = tuple(int(p) for p in scipy.__version__.split(".")[:2] if p.isdigit())
_USE_VARIANT_KWARG = _SCIPY_VERSION >= (1, 17)


def _anderson_darling(
    reference_data: pd.Series,
    current_data: pd.Series,
    feature_type: ColumnType,
    threshold: float,
) -> Tuple[float, bool]:
    samples = [reference_data.values, current_data.values]
    if _USE_VARIANT_KWARG:
        # New scipy API: returns a result object with a `.pvalue` attribute.
        result = anderson_ksamp(samples, variant="midrank")
        p_value = result.pvalue
    else:
        # Legacy 3-tuple: (statistic, critical_values, significance_level).
        p_value = anderson_ksamp(samples)[2]
    return p_value, p_value < threshold


anderson_darling_test = StatTest(
    name="anderson",
    display_name="Anderson-Darling",
    allowed_feature_types=[ColumnType.Numerical],
    default_threshold=0.1,
)

register_stattest(anderson_darling_test, default_impl=_anderson_darling)
