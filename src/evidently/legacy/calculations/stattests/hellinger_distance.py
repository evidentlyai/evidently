"""Hellinger distance of two samples."""

from collections import defaultdict
from math import sqrt
from typing import DefaultDict
from typing import Tuple

import numpy as np
import pandas as pd

from evidently.legacy.calculations.stattests.registry import StatTest
from evidently.legacy.calculations.stattests.registry import register_stattest
from evidently.legacy.core import ColumnType


def _hellinger_distance(
    reference_data: pd.Series,
    current_data: pd.Series,
    feature_type: ColumnType,
    threshold: float,
) -> Tuple[float, bool]:
    """Compute the Hellinger distance between two arrays"""
    reference_data = reference_data.dropna()
    current_data = current_data.dropna()

    if reference_data.empty or current_data.empty:
        return np.nan, False

    keys = list((set(reference_data.unique()) | set(current_data.unique())))

    if feature_type == ColumnType.Categorical:
        dd: DefaultDict[int, int] = defaultdict(int)
        ref = (reference_data.value_counts() / len(reference_data)).to_dict(into=dd)
        curr = (current_data.value_counts() / len(current_data)).to_dict(into=dd)

        hellinger_distance = 0.0
        for key in keys:
            p1 = ref[key]
            p2 = curr[key]
            hellinger_distance += sqrt(float(p1) * float(p2))

        hellinger_distance = np.clip(hellinger_distance, 0, 1)
        hellinger_distance = sqrt(1 - hellinger_distance)

    else:
        bins = np.histogram_bin_edges(keys, bins="sturges")
        h1 = np.histogram(reference_data.to_numpy(), bins=bins, density=True)[0]
        h2 = np.histogram(current_data.to_numpy(), bins=bins, density=True)[0]

        bin_width = (max(bins) - min(bins)) / (len(bins) - 1) if len(bins) > 1 else 1.0

        hellinger_distance = 0.0
        for i in range(len(h1)):
            p1 = h1[i]
            p2 = h2[i]
            hellinger_distance += sqrt(float(p1) * float(p2)) * bin_width

        hellinger_distance = np.clip(hellinger_distance, 0, 1)
        hellinger_distance = sqrt(1 - hellinger_distance)

    return hellinger_distance, hellinger_distance >= threshold


hellinger_stat_test = StatTest(
    name="hellinger",
    display_name="Hellinger distance",
    allowed_feature_types=[ColumnType.Categorical, ColumnType.Numerical],
    default_threshold=0.1,
)

register_stattest(hellinger_stat_test, _hellinger_distance)
