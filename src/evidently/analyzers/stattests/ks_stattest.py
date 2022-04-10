#!/usr/bin/env python
# coding: utf-8
import pandas as pd

from scipy.stats import ks_2samp

from evidently.analyzers.stattests.registry import StatTest, register_stattest


def _ks_stat_test(reference_data: pd.Series, current_data: pd.Series, threshold: float):
    p_value = ks_2samp(reference_data, current_data)[1]
    return p_value, p_value < threshold


ks_stat_test = StatTest(
    name="ks",
    display_name="K-S (p_value)",
    func=_ks_stat_test,
    allowed_feature_types=["num"],
)

register_stattest(ks_stat_test)
