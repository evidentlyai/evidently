#!/usr/bin/env python
# coding: utf-8
import pandas as pd

from scipy.stats import chisquare


def chi_stat_test(reference_data: pd.Series, current_data: pd.Series):
    keys = set(reference_data) | set(current_data)

    ref_feature_dict = {**dict.fromkeys(keys, 0), **dict(reference_data.value_counts())}
    current_feature_dict = {**dict.fromkeys(keys, 0), **dict(current_data.value_counts())}

    k_norm = current_data.shape[0] / reference_data.shape[0]

    f_exp = [value * k_norm for key, value in sorted(ref_feature_dict.items())]
    f_obs = [value for key, value in sorted(current_feature_dict.items())]
    return chisquare(f_exp, f_obs)[1]
