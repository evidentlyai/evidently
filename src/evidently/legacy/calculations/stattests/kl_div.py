"""Kullback-Leibler divergence of two samples."""

from typing import Tuple

import numpy as np
import pandas as pd
from scipy import stats

from evidently.legacy.calculations.stattests.registry import StatTest
from evidently.legacy.calculations.stattests.registry import register_stattest
from evidently.legacy.calculations.stattests.utils import get_binned_data
from evidently.legacy.core import ColumnType


def _kl_div(
    reference_data: pd.Series, current_data: pd.Series, feature_type: ColumnType, threshold: float, n_bins: int = 30
) -> Tuple[float, bool]:
    """Compute the Kullback-Leibler divergence between two arrays"""
    if reference_data.empty or current_data.empty:
        return np.nan, False

    reference_percents, current_percents = get_binned_data(reference_data, current_data, feature_type, n_bins)
    kl_div_value = stats.entropy(reference_percents, current_percents)
    return kl_div_value, kl_div_value >= threshold


kl_div_stat_test = StatTest(
    name="kl_div",
    display_name="Kullback-Leibler divergence",
    allowed_feature_types=[ColumnType.Categorical, ColumnType.Numerical],
    default_threshold=0.1,
)

register_stattest(kl_div_stat_test, _kl_div)
