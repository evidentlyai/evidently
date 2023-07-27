"""Wasserstein distance of two samples.

Name: "wasserstein"

Import:

    >>> from evidently.calculations.stattests import wasserstein_stat_test

Properties:
- only for numerical features
- returns p-value

Example:
    Using by object:

    >>> from evidently.options import DataDriftOptions
    >>> from evidently.calculations.stattests import wasserstein_stat_test
    >>> options = DataDriftOptions(all_features_stattest=wasserstein_stat_test)

    Using by name:

    >>> from evidently.options import DataDriftOptions
    >>> options = DataDriftOptions(all_features_stattest="wasserstein")
"""
from typing import Tuple

from scipy import stats

from evidently.calculations.stattests.registry import StatTest
from evidently.calculations.stattests.registry import register_stattest
from evidently.utils.spark_compat import Series
from evidently.utils.spark_compat import spark_warn


def _wasserstein_distance_norm(
    reference_data: Series, current_data: Series, feature_type: str, threshold: float
) -> Tuple[float, bool]:
    """Compute the first Wasserstein distance between two arrays normed by std of reference data
    Args:
        reference_data: reference data
        current_data: current data
        feature_type: feature type
        threshold: all values above this threshold means data drift
    Returns:
        wasserstein_distance_norm: normed Wasserstein distance
        test_result: whether the drift is detected
    """
    spark_warn(
        reference_data,
        current_data,
        message="Wasserstein distance is not implemented for spark and will collect data to driver",
    )
    norm = max(reference_data.std(), 0.001)  # type: ignore[type-var]
    wd_norm_value = stats.wasserstein_distance(reference_data.to_numpy(), current_data.to_numpy()) / norm
    return wd_norm_value, wd_norm_value >= threshold


wasserstein_stat_test = StatTest(
    name="wasserstein",
    display_name="Wasserstein distance (normed)",
    func=_wasserstein_distance_norm,
    allowed_feature_types=["num"],
    default_threshold=0.1,
)

register_stattest(wasserstein_stat_test)
