from typing import List
from typing import Tuple

import numpy as np
import pandas as pd
from sklearn import metrics

from evidently.calculations.stattests.registry import StatTest
from evidently.calculations.stattests.registry import register_stattest


def _permutation_test(x: pd.Series, y: pd.Series, iterations: int = 100) -> np.ndarray:
    """Permutation test.
    Args:
        x: array_like
        y: array_like
        iterations: int
        threshold: level of significance
    Returns:
        mmds: list of mmd values
    """
    x = x.values
    y = y.values
    len_x = x.shape[0]
    len_y = y.shape[0]
    xy = np.hstack([x, y])
    hold_mmds = []
    for _ in range(iterations):
        x_samp = np.random.choice(xy, len_x)
        y_samp = np.random.choice(xy, len_y)
        mmd_res = _emperical_mmd_rbf(x=pd.Series(x_samp), y=pd.Series(y_samp))
        hold_mmds.append(mmd_res)
    return np.array(hold_mmds)


def _emperical_mmd_rbf(x: pd.Series, y: pd.Series) -> float:
    """Maximum Mean Discrepancy (MMD) test
    Args:
        x: pandas series
        y: pandas series
    Returns:
        mmd_distance: float
    """
    m = x.shape[0]
    n = y.shape[0]
    x = x.values.reshape(-1, 1)
    y = y.values.reshape(-1, 1)
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

    return mmd_res


def _mmd_stattest(
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
    mmd_res = _emperical_mmd_rbf(x=reference_data, y=current_data)
    get_mmds = _permutation_test(x=reference_data, y=current_data, iterations=100)
    p_value = np.mean(mmd_res <= get_mmds)
    return p_value, p_value < threshold


emperical_mmd = StatTest(
    name="emperical_mmd",
    display_name="emperical_mmd",
    func=_mmd_stattest,
    allowed_feature_types=["num"],
    default_threshold=0.1,
)

register_stattest(emperical_mmd)
