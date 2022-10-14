from typing import List
from typing import Tuple

import numpy as np
import pandas as pd
from sklearn import metrics

from evidently.calculations.stattests.registry import StatTest
from evidently.calculations.stattests.registry import register_stattest


def _permutation_test(x: np.ndarray, y: np.ndarray, iterations: int = 100) -> List[float]:
    """Permutation test.
    Args:
        x: array_like
        y: array_like
        iterations: int
        threshold: level of significance
    Returns:
        mmds: list of mmd values
    """
    len_x = x.shape[0]
    len_y = y.shape[0]
    xy = np.hstack([x, y])
    hold_mmds = []
    for _ in range(iterations):
        x_samp = np.random.choice(xy, len_x)
        y_samp = np.random.choice(xy, len_y)
        mmd_res = _emperical_mmd_rbf(
            reference_data=pd.Series(x_samp),
            current_data=pd.Series(y_samp),
            feature_type="cat",
            threshold=0.1,
        )[0]
        hold_mmds.append(mmd_res)
    return hold_mmds


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
    x = reference_data.values.reshape(-1, 1)
    y = current_data.values.reshape(-1, 1)
    sigma = np.median(metrics.pairwise_distances(x.reshape(-1, 1), y.reshape(-1, 1), metric="euclidean")) ** 2
    gamma = 1 / sigma
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
    return mmd_res, mmd_res < threshold


emperical_mmd = StatTest(
    name="emperical_mmd",
    display_name="emperical_mmd",
    func=_emperical_mmd_rbf,
    allowed_feature_types=["num"],
    default_threshold=0.1,
)

register_stattest(emperical_mmd)
