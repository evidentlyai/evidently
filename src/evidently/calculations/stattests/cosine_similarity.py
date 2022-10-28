from typing import Tuple

import numpy as np
import pandas as pd

from evidently.calculations.stattests.registry import StatTest
from evidently.calculations.stattests.registry import register_stattest


def _cosine_similarity(
    reference_data: pd.Series,
    current_data: pd.Series,
    feature_type: str,
    threshold: float,
) -> Tuple[float, bool]:
    """Run the  Anderson-Darling test of two samples.
    Args:
        reference_data: reference data
        current_data: current data
        feature_type: feature type
        threshold: level of significance
    Returns:
        p_value: p-value
        test_result: whether the drift is detected
    """
    reference_correlation = np.cov(reference_data) / (
        np.var(reference_data.values.flatten())
        * np.var(reference_data.values.flatten())
    )
    current_correlation = np.cov(current_data) / (
        np.var(current_data.values.flatten()) * np.var(current_data.values.flatten())
    )

    T0 = 1 - np.sum(reference_correlation * current_correlation) / (
        np.linalg.norm(reference_correlation, ord="fro")
        * np.linalg.norm(current_correlation, ord="fro")
    )

    stacked_correlation = np.concatenate(
        [reference_data.values, current_data.values], axis=0
    )

    Ti = []
    permutations = 100
    for i in range(permutations):
        idxs = np.arange(len(stacked_correlation))
        np.random.shuffle(idxs)
        shuffled_stacked = stacked_correlation[idxs]
        reference_rows_data = shuffled_stacked[: reference_correlation.shape[0]]
        current_rows_data = shuffled_stacked[reference_correlation.shape[0] :]
        reference_rows_correlation = np.cov(reference_rows_data) / (
            np.var(reference_rows_data.flatten())
            * np.var(reference_rows_data.flatten())
        )
        current_rows_correlation = np.cov(current_rows_data) / (
            np.var(current_rows_data.flatten()) * np.var(current_rows_data.flatten())
        )
        Ti.append(
            1
            - np.sum(reference_rows_correlation * current_rows_correlation)
            / (
                np.linalg.norm(reference_rows_correlation, ord="fro")
                * np.linalg.norm(current_rows_correlation, ord="fro")
            )
        )

    p_value = (
        (np.nansum(np.array(Ti) >= T0) + 1) / (10 + 1)
        if np.isnan(np.array(Ti)).sum() == 0
        else np.nan
    )
    return p_value, p_value < threshold


cosine_similarity_test = StatTest(
    name="cosine_similarity",
    display_name="Cosine-Similarity",
    func=_cosine_similarity,
    allowed_feature_types=["num"],
    default_threshold=0.1,
)


register_stattest(cosine_similarity_test)
