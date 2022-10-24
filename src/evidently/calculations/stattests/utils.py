from collections import Counter

import numpy as np
import pandas as pd


def get_unique_not_nan_values_list_from_series(current_data: pd.Series, reference_data: pd.Series) -> list:
    """Get unique values from current and reference series, drop NaNs"""
    return list(set(reference_data.dropna().unique()) | set(current_data.dropna().unique()))


def get_binned_data(
    reference_data: pd.Series, current_data: pd.Series, feature_type: str, n: int, feel_zeroes: bool = True
):
    """Split variable into n buckets based on reference quantiles
    Args:
        reference_data: reference data
        current_data: current data
        feature_type: feature type
        n: number of quantiles
    Returns:
        reference_percents: % of records in each bucket for reference
        current_percents: % of records in each bucket for current
    """
    n_vals = reference_data.nunique()

    if feature_type == "num" and n_vals > 20:
        bins = np.histogram_bin_edges(list(reference_data) + list(current_data), bins="sturges")
        reference_percents = np.histogram(reference_data, bins)[0] / len(reference_data)
        current_percents = np.histogram(current_data, bins)[0] / len(current_data)

    else:
        keys = get_unique_not_nan_values_list_from_series(current_data=current_data, reference_data=reference_data)
        ref_feature_dict = {**dict.fromkeys(keys, 0), **dict(reference_data.value_counts())}
        current_feature_dict = {**dict.fromkeys(keys, 0), **dict(current_data.value_counts())}
        reference_percents = np.array([ref_feature_dict[key] / len(reference_data) for key in keys])
        current_percents = np.array([current_feature_dict[key] / len(current_data) for key in keys])

    if feel_zeroes:
        np.place(reference_percents, reference_percents == 0, 0.0001)
        np.place(current_percents, current_percents == 0, 0.0001)

    return reference_percents, current_percents


def permutation_test(reference_data, current_data, observed, test_statistic_func, iterations=100):

    """Perform a two-sided permutation test
    Args:
        reference_data: reference data
        current_data: current data
        observed: observed value
        test_statistic_func: the test statistic function
        iterations: number of times to permute
    Returns:
        p_value: two-sided p_value
    """
    np.random.seed(0)
    hold_test_statistic = []
    for i in range(iterations):
        combined_data = reference_data.tolist() + current_data.tolist()
        new_reference = np.random.choice(combined_data, len(reference_data), replace=False).tolist()
        count_combined = Counter(combined_data)
        count_new_reference = Counter(new_reference)
        new_current = list((count_combined - count_new_reference).elements())
        hold_test_statistic.append(test_statistic_func(pd.Series(new_reference), pd.Series(new_current)))

    p_val = sum(observed <= abs(np.array(hold_test_statistic))) / len(hold_test_statistic)
    return p_val
