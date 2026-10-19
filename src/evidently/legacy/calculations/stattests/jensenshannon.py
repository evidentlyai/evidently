"""Jensen-Shannon distance of two samples."""

from typing import Optional
from typing import Tuple

import numpy as np
import pandas as pd
from scipy.spatial import distance

from evidently.legacy.calculations.stattests.registry import StatTest
from evidently.legacy.calculations.stattests.registry import register_stattest
from evidently.legacy.calculations.stattests.utils import get_binned_data
from evidently.legacy.core import ColumnType


def _jensenshannon(
    reference_data: pd.Series,
    current_data: pd.Series,
    feature_type: ColumnType,
    threshold: float,
    n_bins: int = 30,
    base: Optional[float] = None,
) -> Tuple[float, bool]:
    """Compute the Jensen-Shannon distance between two arrays"""
    if reference_data.empty or current_data.empty:
        return np.nan, False

    reference_percents, current_percents = get_binned_data(reference_data, current_data, feature_type, n_bins, False)
    jensenshannon_value = distance.jensenshannon(reference_percents, current_percents, base)
    return jensenshannon_value, jensenshannon_value >= threshold


jensenshannon_stat_test = StatTest(
    name="jensenshannon",
    display_name="Jensen-Shannon distance",
    allowed_feature_types=[ColumnType.Categorical, ColumnType.Numerical],
    default_threshold=0.1,
)

register_stattest(jensenshannon_stat_test, _jensenshannon)
