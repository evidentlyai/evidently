"""Cramer-Von-mises test of two samples.

Name: "cramer_von_mises"

Import:

    >>> from evidently.calculations.stattests import cramer_von_mises

Properties:
- only for numerical features
- returns p-value

Example:
    Using by object:

    >>> from evidently.options import DataDriftOptions
    >>> from evidently.calculations.stattests import cramer_von_mises
    >>> options = DataDriftOptions(all_features_stattest=cramer_von_mises)

    Using by name:

    >>> from evidently.options import DataDriftOptions
    >>> options = DataDriftOptions(all_features_stattest="cramer_von_mises")
"""
from itertools import combinations
from typing import Generator
from typing import Tuple

import numpy as np
import pandas as pd
from scipy.special import gammaln
from scipy.special import kv
from scipy.stats import rankdata

from evidently.calculations.stattests.registry import StatTest
from evidently.calculations.stattests.registry import register_stattest


def _all_partitions(nx: int, ny: int) -> Generator[Tuple[int, int], None, None]:
    """
    Args:
        nx: int
        ny: int
    Return:
        None
    """
    z = np.arange(nx + ny)
    for c in combinations(z, nx):
        x = np.array(c)
        mask = np.ones(nx + ny, bool)
        mask[x] = False
        y = z[mask]
        yield x, y


def _pval_cvm_2samp_exact(s: float, nx: int, ny: int):
    """Compute the exact p
    Args:
        s: test statistic
        nx: sample size
        ny: sample size
    Returns:
        p_value: p_value
    """
    rangex = np.arange(nx)
    rangey = np.arange(ny)

    us = []

    for x, y in _all_partitions(nx, ny):
        u = nx * np.sum((x - rangex) ** 2)
        u += ny * np.sum((y - rangey) ** 2)
        us.append(u)

    u, cnt = np.unique(us, return_counts=True)
    p_value = np.sum(cnt[u >= s]) / np.sum(cnt)
    return p_value


class CramerVonMisesResult:
    def __init__(self, statistic, pvalue):
        self.statistic = statistic
        self.pvalue = pvalue

    def __repr__(self):
        return f"{self.__class__.__name__}(statistic={self.statistic}, " f"pvalue={self.pvalue})"


def _cdf_cvm_inf(x: float) -> float:
    """Calculate the cdf of the Cramér-von Mises statistic
    Args:
        x: float
    Returns:
        tot: float
    """
    x = np.asarray(x)

    def term(x, k):
        u = np.exp(gammaln(k + 0.5) - gammaln(k + 1)) / (np.pi**1.5 * np.sqrt(x))
        y = 4 * k + 1
        q = y**2 / (16 * x)
        b = kv(0.25, q)
        return u * np.sqrt(y) * np.exp(-q) * b

    tot = np.zeros_like(x, dtype="float")
    cond = np.ones_like(x, dtype="bool")
    k = 0
    while np.any(cond):
        z = term(x[cond], k)  # type: ignore
        tot[cond] = tot[cond] + z
        cond[cond] = np.abs(z) >= 1e-7
        k += 1

    return tot


def _cvm_2samp(x: np.ndarray, y: np.ndarray, method: str = "auto") -> CramerVonMisesResult:
    """Perform the two-sample Cramér-von Mises test
    Args:
        x : array_like
        y : array_like
        method : {'auto', 'asymptotic', 'exact'}, optional
    Returns:
        res : object with attributes
        statistic : Cramér-von Mises statistic.
        pvalue : float
    """

    xa = np.sort(np.asarray(x))
    ya = np.sort(np.asarray(y))

    if xa.size <= 1 or ya.size <= 1:
        raise ValueError("x and y must contain at least two observations.")
    if xa.ndim > 1 or ya.ndim > 1:
        raise ValueError("The samples must be one-dimensional.")
    if method not in ["auto", "exact", "asymptotic"]:
        raise ValueError("method must be either auto, exact or asymptotic.")

    nx = len(xa)
    ny = len(ya)

    if method == "auto":
        if max(nx, ny) > 10:
            method = "asymptotic"
        else:
            method = "exact"

    z = np.concatenate([xa, ya])
    r = rankdata(z, method="average")

    rx = r[:nx]
    ry = r[nx:]

    u = nx * np.sum((rx - np.arange(1, nx + 1)) ** 2)

    u += ny * np.sum((ry - np.arange(1, ny + 1)) ** 2)

    k, N = nx * ny, nx + ny
    t = u / (k * N) - (4 * k - 1) / (6 * N)

    if method == "exact":
        p = _pval_cvm_2samp_exact(u, nx, ny)
    else:
        et = (1 + 1 / N) / 6

        vt = (N + 1) * (4 * k * N - 3 * (nx**2 + ny**2) - 2 * k)
        vt = vt / (45 * N**2 * 4 * k)  # type: ignore

        tn = 1 / 6 + (t - et) / np.sqrt(45 * vt)

        if tn < 0.003:
            p = 1.0
        else:
            p = max(0, 1.0 - _cdf_cvm_inf(tn))

    return CramerVonMisesResult(statistic=t, pvalue=p)


def _cramer_von_mises(
    reference_data: pd.Series,
    current_data: pd.Series,
    feature_type: str,
    threshold: float,
) -> Tuple[float, bool]:
    """Run the two-sample Cramer-Von-mises test of two samples.
    Args:
        reference_data: reference data
        current_data: current data
        feature_type: feature type
        threshold: level of significance
    Returns:
        p_value: p-value
        test_result: whether the drift is detected
    """
    res = _cvm_2samp(reference_data, current_data)
    return res.pvalue, res.pvalue <= threshold


cramer_von_mises = StatTest(
    name="cramer_von_mises",
    display_name="Cramer-Von-mises",
    func=_cramer_von_mises,
    allowed_feature_types=["num"],
    default_threshold=0.1,
)

register_stattest(cramer_von_mises)
