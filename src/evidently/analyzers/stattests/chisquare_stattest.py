#!/usr/bin/env python
# coding: utf-8
import numpy as np
import pandas as pd

from scipy.stats import chisquare


def chi_stat_test(reference_data: pd.Series, current_data: pd.Series) -> float:
    #  TODO: simplify ignoring NaN values here, in z_stat_test and data_drift_analyzer
    keys = list((set(reference_data) | set(current_data)) - {np.nan})

    ref_feature_dict = {**dict.fromkeys(keys, 0), **dict(reference_data.value_counts())}
    current_feature_dict = {**dict.fromkeys(keys, 0), **dict(current_data.value_counts())}

    k_norm = current_data.shape[0] / reference_data.shape[0]

    f_exp = [ref_feature_dict[key] * k_norm for key in keys]
    f_obs = [current_feature_dict[key] for key in keys]
    return chisquare(f_exp, f_obs)[1]
