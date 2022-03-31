#!/usr/bin/env python
# coding: utf-8
import pandas as pd

from scipy.stats import ks_2samp

from evidently.analyzers.stattests.registry import stattest


@stattest("ks", allowed_feature_types=["num"])
def ks_stat_test(reference_data: pd.Series, current_data: pd.Series):
    return ks_2samp(reference_data, current_data)[1]
