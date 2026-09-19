import numpy as np
import pandas as pd
import pytest

from evidently.legacy.calculations.regression_performance import calculate_regression_performance
from evidently.legacy.metric_results import DatasetColumns
from evidently.legacy.metric_results import DatasetUtilityColumns


def _make_dataset(near_zero_indices, n_rows=10, target_value=0.0):
    rng = np.random.default_rng(42)
    target = rng.normal(loc=10.0, scale=1.0, size=n_rows)
    target[list(near_zero_indices)] = target_value
    prediction = target + rng.normal(scale=0.1, size=n_rows)
    return pd.DataFrame(
        {
            "target": target,
            "prediction": prediction,
            "feature": rng.normal(size=n_rows),
        }
    )


def _columns():
    return DatasetColumns(
        utility_columns=DatasetUtilityColumns(target="target", prediction="prediction"),
        num_feature_names=["feature"],
        cat_feature_names=[],
        text_feature_names=[],
        datetime_feature_names=[],
        target_type="num",
        task="regression",
    )


def test_near_zero_values_counts_rows_not_cells():
    """``near_zero_values`` is a row counter, so it must not scale with the number of columns."""
    near_zero_indices = [2, 5, 9]
    dataset = _make_dataset(near_zero_indices)

    result = calculate_regression_performance(dataset, _columns(), error_bias_prefix="")

    assert result.near_zero_values == len(near_zero_indices)


def test_near_zero_values_with_custom_epsilon_and_drop_handling():
    near_zero_indices = [0, 3, 4, 7]
    dataset = _make_dataset(near_zero_indices, target_value=1e-9)
    epsilon = 1e-6

    result = calculate_regression_performance(
        dataset,
        _columns(),
        error_bias_prefix="",
        mape_zero_handling="drop",
        mape_epsilon=epsilon,
    )

    assert result.near_zero_values == len(near_zero_indices)


def test_near_zero_values_is_zero_when_no_target_is_near_zero():
    dataset = _make_dataset([])

    result = calculate_regression_performance(dataset, _columns(), error_bias_prefix="")

    assert result.near_zero_values == 0


@pytest.mark.parametrize("zero_handling", ["none", "drop", "replace"])
def test_near_zero_values_independent_of_zero_handling(zero_handling):
    near_zero_indices = [1, 6]
    dataset = _make_dataset(near_zero_indices)

    result = calculate_regression_performance(
        dataset,
        _columns(),
        error_bias_prefix="",
        mape_zero_handling=zero_handling,
        mape_replace_value=1.0,
    )

    assert result.near_zero_values == len(near_zero_indices)
