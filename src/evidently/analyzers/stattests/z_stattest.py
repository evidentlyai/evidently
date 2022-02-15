#!/usr/bin/env python
# coding: utf-8
import numpy as np
import pandas as pd

from scipy.stats import norm


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


def z_stat_test(reference_data: pd.Series, current_data: pd.Series) -> float:
    #  TODO: simplify ignoring NaN values here, in chi_stat_test and data_drift_analyzer
    keys = set(list(reference_data.unique()) + list(current_data.unique())) - {np.nan}
    ordered_keys = sorted(list(keys))
    return proportions_diff_z_test(
        proportions_diff_z_stat_ind(
            reference_data.apply(lambda x, key=ordered_keys[0]: 0 if x == key else 1),
            current_data.apply(lambda x, key=ordered_keys[0]: 0 if x == key else 1)
        )
    )
