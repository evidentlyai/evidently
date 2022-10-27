from itertools import product

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
        np.place(
            reference_percents,
            reference_percents == 0,
            min(reference_percents[reference_percents != 0]) / 10**6
            if min(reference_percents[reference_percents != 0]) <= 0.0001
            else 0.0001,
        )
        np.place(
            current_percents,
            current_percents == 0,
            min(current_percents[current_percents != 0]) / 10**6
            if min(current_percents[current_percents != 0]) <= 0.0001
            else 0.0001,
        )

    return reference_percents, current_percents


def generate_fisher2x2_contingency_table(reference_data: pd.Series, current_data: pd.Series) -> np.ndarray:
    """Generate 2x2 contingency matrix for fisher exact test
    Args:
        reference_data: reference data
        current_data: current data
    Raises:
        ValueError: if reference_data and current_data are not of equal length
    Returns:
        contingency_matrix: contingency_matrix for binary data
    """
    if reference_data.shape[0] != current_data.shape[0]:
        raise ValueError(
            "reference_data and current_data are not of equal length, please ensure that they are of equal length"
        )
    unique_categories = set(reference_data.unique().tolist() + current_data.unique().tolist())
    if len(unique_categories) != 2:
        unique_categories.add("placeholder")

    unique_categories = list(unique_categories)  # type: ignore
    unique_categories = dict(zip(unique_categories, [0, 1]))  # type: ignore

    reference_data = reference_data.map(unique_categories).values
    current_data = current_data.map(unique_categories).values

    zero_ref = reference_data.size - np.count_nonzero(reference_data)
    one_ref = np.count_nonzero(reference_data)

    zero_cur = current_data.size - np.count_nonzero(current_data)
    one_cur = np.count_nonzero(current_data)

    contingency_table = np.array([[one_cur, zero_cur], [one_ref, zero_ref]])

    return contingency_table
