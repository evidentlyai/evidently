import pandas as pd
import numpy as np


def get_binned_data(reference: pd.Series, current: pd.Series, feature_type: str, n: int, feel_zeroes: bool = True):
    """Split variable into n buckets based on reference quantiles
    Args:
        reference: reference data
        current: current data
        feature_type: feature type
        n: number of quantiles
    Returns:
        reference_percents: % of records in each bucket for reference
        current_percents: % of records in each bucket for reference
    """
    n_vals = reference.nunique()
    if feature_type == 'num' and n_vals > 20:

        bins = np.histogram_bin_edges(list(reference) + list(current), bins='sturges')

        reference_percents = np.histogram(reference, bins)[0] / len(reference)
        current_percents = np.histogram(current, bins)[0] / len(current)

    else:
        keys = list((set(reference.unique()) | set(current.unique())) - {np.nan})

        ref_feature_dict = {**dict.fromkeys(keys, 0), **dict(reference.value_counts())}
        current_feature_dict = {**dict.fromkeys(keys, 0), **dict(current.value_counts())}

        reference_percents = np.array([ref_feature_dict[key] / len(reference) for key in keys])
        current_percents = np.array([current_feature_dict[key] / len(current) for key in keys])
    if feel_zeroes:
        np.place(reference_percents, reference_percents == 0, 0.0001)
        np.place(current_percents, current_percents == 0, 0.0001)

    return reference_percents, current_percents
