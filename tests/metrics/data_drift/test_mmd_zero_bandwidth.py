import numpy as np
import pandas as pd
import pytest

from evidently.legacy.metrics.data_drift.embedding_drift_methods import mmd


@pytest.mark.parametrize("bootstrap", [False, True])
@pytest.mark.parametrize("constant", [0.0, 7.0])
def test_identical_constant_embeddings_have_zero_mmd(bootstrap, constant):
    sample = pd.DataFrame(np.full((10, 2), constant))

    with np.errstate(divide="raise", invalid="raise"):
        score, drifted, method = mmd(bootstrap=bootstrap)(sample, sample)

    assert score == 0.0
    assert not drifted
    assert method == "mmd"


@pytest.mark.parametrize("bootstrap", [False, True])
def test_constant_reference_detects_a_changed_embedding(bootstrap):
    reference = pd.DataFrame(np.zeros((10, 2)))
    current = pd.DataFrame(np.ones((10, 2)))

    with np.errstate(divide="raise", invalid="raise"):
        score, drifted, method = mmd(bootstrap=bootstrap)(current, reference)

    assert score == pytest.approx(2 * (1 - np.exp(-1)))
    assert drifted
    assert method == "mmd"


def test_zero_median_bandwidth_retains_distinct_embedding_groups():
    reference = pd.DataFrame({"value": [0.0] * 9 + [2.0]})
    current = pd.DataFrame({"value": [0.0] * 6 + [2.0] * 4})

    with np.errstate(divide="raise", invalid="raise"):
        score, drifted, method = mmd()(current, reference)

    # The zero-bandwidth limit has kernel 1 for equal vectors and 0 otherwise.
    within_reference = 9 * 8 / (10 * 9)
    within_current = (6 * 5 + 4 * 3) / (10 * 9)
    between = (9 * 6 + 1 * 4) / (10 * 10)
    expected = within_reference + within_current - 2 * between
    assert score == pytest.approx(expected)
    assert drifted
    assert method == "mmd"


def test_positive_bandwidth_keeps_the_rbf_statistic():
    reference = pd.DataFrame({"value": [0.0, 1.0, 2.0]})
    current = pd.DataFrame({"value": [3.0, 4.0, 5.0]})
    values = np.arange(6.0)
    kernel = np.exp(-((values[:, None] - values[None, :]) ** 2) / 9.0)
    within_reference = sum(kernel[i, j] for i in range(3) for j in range(3) if i != j) / 6
    within_current = sum(kernel[i, j] for i in range(3, 6) for j in range(3, 6) if i != j) / 6
    between = sum(kernel[i, j] for i in range(3) for j in range(3, 6)) / 9

    score, drifted, _ = mmd()(current, reference)

    assert score == pytest.approx(within_reference + within_current - 2 * between)
    assert drifted
