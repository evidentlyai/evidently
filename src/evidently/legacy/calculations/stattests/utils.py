from collections import Counter
from typing import Any
from typing import Set

import numpy as np
import pandas as pd

from evidently.legacy.core import ColumnType


def get_unique_not_nan_values_list_from_series(current_data: pd.Series, reference_data: pd.Series) -> list:
    """Get unique values from current and reference series, drop NaNs"""
    return list(set(reference_data.dropna().unique()) | set(current_data.dropna().unique()))


def get_binned_data(
    reference_data: pd.Series, current_data: pd.Series, feature_type: ColumnType, n: int, feel_zeroes: bool = True
):
    """Split variable into n buckets based on reference quantiles"""
    n_vals = reference_data.nunique()

    if feature_type == ColumnType.Numerical and n_vals > 20:
        combined = np.asarray(pd.concat([reference_data, current_data], axis=0).values)
        bins = np.histogram_bin_edges(combined, bins="sturges")
        reference_percents = np.histogram(reference_data, bins)[0] / len(reference_data) if len(reference_data) > 0 else np.array([])
        current_percents = np.histogram(current_data, bins)[0] / len(current_data) if len(current_data) > 0 else np.array([])

    else:
        keys = get_unique_not_nan_values_list_from_series(current_data=current_data, reference_data=reference_data)
        ref_feature_dict = {**dict.fromkeys(keys, 0), **dict(reference_data.value_counts())}
        current_feature_dict = {**dict.fromkeys(keys, 0), **dict(current_data.value_counts())}
        reference_percents = np.array([ref_feature_dict[key] / len(reference_data) if len(reference_data) > 0 else 0.0 for key in keys])
        current_percents = np.array([current_feature_dict[key] / len(current_data) if len(current_data) > 0 else 0.0 for key in keys])

    if feel_zeroes:
        ref_nz = reference_percents[reference_percents != 0]
        ref_fill = (min(ref_nz) / 10**6 if min(ref_nz) <= 0.0001 else 0.0001) if ref_nz.size > 0 else 0.0001
        np.place(reference_percents, reference_percents == 0, ref_fill)

        curr_nz = current_percents[current_percents != 0]
        curr_fill = (min(curr_nz) / 10**6 if min(curr_nz) <= 0.0001 else 0.0001) if curr_nz.size > 0 else 0.0001
        np.place(current_percents, current_percents == 0, curr_fill)

    return reference_percents, current_percents


def permutation_test(reference_data, current_data, observed, test_statistic_func, iterations=100):
    """Perform a two-sided permutation test"""
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


def generate_fisher2x2_contingency_table(reference_data: pd.Series, current_data: pd.Series) -> np.ndarray:
    """Generate 2x2 contingency matrix for fisher exact test"""
    if reference_data.shape[0] != current_data.shape[0]:
        raise ValueError(
            "reference_data and current_data are not of equal length, please ensure that they are of equal length"
        )
    unique_categories: Set[Any] = set(reference_data.unique().tolist() + current_data.unique().tolist())
    if len(unique_categories) != 2:
        unique_categories.add("placeholder")

    unique_categories_mapping = dict(zip(list(unique_categories), [0, 1]))

    ref_data = reference_data.map(unique_categories_mapping).to_numpy()
    curr_data = current_data.map(unique_categories_mapping).to_numpy()

    zero_ref = ref_data.size - np.count_nonzero(ref_data)
    one_ref = np.count_nonzero(ref_data)

    zero_cur = curr_data.size - np.count_nonzero(curr_data)
    one_cur = np.count_nonzero(curr_data)

    contingency_table = np.array([[one_cur, zero_cur], [one_ref, zero_ref]])

    return contingency_table
