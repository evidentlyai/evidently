from typing import Tuple

import numpy as np
import pandas as pd
from sklearn import metrics

from evidently.calculations.stattests.registry import StatTest
from evidently.calculations.stattests.registry import register_stattest


def _bootstrap_results():
    # performs bootstrapping
    pass


def _emperical_mmd_rbf(
    reference_data: pd.Series,
    current_data: pd.Series,
    feature_type: str,
    threshold: float,
) -> Tuple[float, bool]:
    """Run the  emperical maximum mean discrepancy test.
    Args:
        reference_data: reference data
        current_data: current data
        feature_type: feature type
        threshold: level of significance
    Returns:
        p_value: p-value
        test_result: whether the drift is detected
    """
    m = reference_data.shape[0]
    n = current_data.shape[0]
    x = reference_data.values
    y = current_data.values
    gamma = 1
    Kxx = metrics.pairwise.rbf_kernel(x, x, gamma)
    Kyy = metrics.pairwise.rbf_kernel(y, y, gamma)
    Kxy = metrics.pairwise.rbf_kernel(x, y, gamma)

    t1 = 1 / (m * (m - 1))
    t2 = 1 / (n * (n - 1))
    t3 = 1 / (m * n)
    A = np.sum(Kxx - np.diag(np.diagonal(Kxx)))
    B = np.sum(Kyy - np.diag(np.diagonal(Kyy)))
    C = np.sum(Kxy)
    mmd_res = (t1 * A) + (t2 * B) - (2 * t3 * C)
    p_value = mmd_res

    return p_value, p_value < threshold


emperical_mmd = StatTest(
    name="emperical_mmd",
    display_name="emperical_mmd",
    func=_emperical_mmd_rbf,
    allowed_feature_types=["num"],
    default_threshold=0.1,
)

register_stattest(emperical_mmd)
