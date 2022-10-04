from typing import Tuple

import pandas as pd
import numpy as np
import scipy
from itertools import combinations
from scipy.special import gamma, kv, gammaln

from evidently.calculations.stattests.registry import StatTest
from evidently.calculations.stattests.registry import register_stattest


def _all_partitions(nx, ny):
    z = np.arange(nx + ny)
    for c in combinations(z, nx):
        x = np.array(c)
        mask = np.ones(nx + ny, bool)
        mask[x] = False
        y = z[mask]
        yield x, y


def _pval_cvm_2samp_exact(s, nx, ny):
    rangex = np.arange(nx)
    rangey = np.arange(ny)

    us = []

    for x, y in _all_partitions(nx, ny):
        u = nx * np.sum((x - rangex) ** 2)
        u += ny * np.sum((y - rangey) ** 2)
        us.append(u)

    u, cnt = np.unique(us, return_counts=True)
    return np.sum(cnt[u >= s]) / np.sum(cnt)


class CramerVonMisesResult:
    def __init__(self, statistic, pvalue):
        self.statistic = statistic
        self.pvalue = pvalue

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(statistic={self.statistic}, "
            f"pvalue={self.pvalue})"
        )


def _cdf_cvm_inf(x):

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
        z = term(x[cond], k)
        tot[cond] = tot[cond] + z
        cond[cond] = np.abs(z) >= 1e-7
        k += 1

    return tot


def CVM_2samp(x, y, method="auto"):
    xa = np.sort(np.asarray(x))
    ya = np.sort(np.asarray(y))

    nx = len(xa)
    ny = len(ya)

    if method == "auto":
        if max(nx, ny) > 10:
            method = "asymptotic"
        else:
            method = "exact"

    z = np.concatenate([xa, ya])
    r = scipy.stats.rankdata(z, method="average")
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
        vt = vt / (45 * N**2 * 4 * k)

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
    res = CVM_2samp(reference_data, current_data)
    return res.pvalue, res.pvalue <= threshold


cramer_von_mises = StatTest(
    name="cramer_von_mises",
    display_name="cramer_von_mises",
    func=_cramer_von_mises,
    allowed_feature_types=["num"],
)

register_stattest(cramer_von_mises)
