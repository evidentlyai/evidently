#!/usr/bin/env python
# coding: utf-8
import pandas as pd

from scipy.stats import chisquare


def chi_stat_test(reference_data: pd.DataFrame, current_data: pd.DataFrame):
    ref_feature_vc = reference_data.value_counts()
    current_feature_vc = current_data.value_counts()
    keys = set(list(reference_data.unique()) + list(current_data.unique()))

    ref_feature_dict = dict.fromkeys(keys, 0)
    for key, item in zip(ref_feature_vc.index, ref_feature_vc.values):
        ref_feature_dict[key] = item

    current_feature_dict = dict.fromkeys(keys, 0)
    for key, item in zip(current_feature_vc.index, current_feature_vc.values):
        current_feature_dict[key] = item
    f_exp = [value[1] for value in sorted(ref_feature_dict.items())]
    f_obs = [value[1] for value in sorted(current_feature_dict.items())]
    return chisquare(f_exp, f_obs)[1]
