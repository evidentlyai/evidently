#!/usr/bin/env python
# coding: utf-8
from typing import Tuple

import numpy as np
import pandas as pd

from scipy.stats import norm

from evidently.analyzers.stattests.registry import StatTest, register_stattest


def proportions_diff_z_stat_ind(ref: pd.DataFrame, curr: pd.DataFrame):
    # pylint: disable=invalid-name
    n1 = len(ref)
    n2 = len(curr)

    p1 = float(sum(ref)) / n1
    p2 = float(sum(curr)) / n2
    P = float(p1 * n1 + p2 * n2) / (n1 + n2)

    return (p1 - p2) / np.sqrt(P * (1 - P) * (1. / n1 + 1. / n2))


def proportions_diff_z_test(z_stat, alternative='two-sided'):
    if alternative == 'two-sided':
        return 2 * (1 - norm.cdf(np.abs(z_stat)))

    if alternative == 'less':
        return norm.cdf(z_stat)

    if alternative == 'greater':
        return 1 - norm.cdf(z_stat)

    raise ValueError("alternative not recognized\n"
                     "should be 'two-sided', 'less' or 'greater'")


def _z_stat_test(
        reference_data: pd.Series,
        current_data: pd.Series,
        feature_type: str,
        threshold: float) -> Tuple[float, bool]:
    #  TODO: simplify ignoring NaN values here, in chi_stat_test and data_drift_analyzer
    if (reference_data.nunique() == 1
            and current_data.nunique() == 1
            and reference_data.unique()[0] == current_data.unique()[0]):
        p_value = 1
    else:
        keys = set(list(reference_data.unique()) + list(current_data.unique())) - {np.nan}
        ordered_keys = sorted(list(keys))
        p_value = proportions_diff_z_test(
            proportions_diff_z_stat_ind(
                reference_data.apply(lambda x, key=ordered_keys[0]: 0 if x == key else 1),
                current_data.apply(lambda x, key=ordered_keys[0]: 0 if x == key else 1)
            )
        )
    return p_value, p_value < threshold


z_stat_test = StatTest(
    name="z",
    display_name="Z-test p_value",
    func=_z_stat_test,
    allowed_feature_types=["cat"],
)

register_stattest(z_stat_test)
