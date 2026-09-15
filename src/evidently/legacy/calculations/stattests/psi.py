"""PSI of two samples."""

from typing import Tuple

import numpy as np
import pandas as pd

from evidently.legacy.calculations.stattests.registry import StatTest
from evidently.legacy.calculations.stattests.registry import register_stattest
from evidently.legacy.calculations.stattests.utils import get_binned_data
from evidently.legacy.core import ColumnType


def _psi(
    reference_data: pd.Series, current_data: pd.Series, feature_type: ColumnType, threshold: float, n_bins: int = 30
) -> Tuple[float, bool]:
    """Calculate the PSI"""
    if reference_data.empty or current_data.empty:
        return np.nan, False

    reference_percents, current_percents = get_binned_data(reference_data, current_data, feature_type, n_bins)

    psi_values = (reference_percents - current_percents) * np.log(reference_percents / current_percents)
    psi_value = np.sum(psi_values)

    return psi_value, psi_value >= threshold


psi_stat_test = StatTest(
    name="psi",
    display_name="PSI",
    allowed_feature_types=[ColumnType.Categorical, ColumnType.Numerical],
    default_threshold=0.1,
)

register_stattest(psi_stat_test, _psi)
