import numpy as np
import pandas as pd
import pytest
from sklearn.metrics import roc_auc_score

from evidently.legacy.metrics.data_drift.embedding_drift_methods import calc_roc_auc_random
from evidently.legacy.metrics.data_drift.embedding_drift_methods import distance
from evidently.legacy.metrics.data_drift.embedding_drift_methods import mmd
from evidently.legacy.metrics.data_drift.embedding_drift_methods import model


@pytest.fixture(autouse=True)
def restore_global_random_state():
    state = np.random.get_state()
    yield
    np.random.set_state(state)


def _embeddings():
    rng = np.random.default_rng(17)
    reference = pd.DataFrame(rng.normal(size=(20, 3)))
    current = pd.DataFrame(rng.normal(loc=0.2, size=(24, 3)))
    return current, reference


@pytest.mark.parametrize("method", [distance, mmd, model])
@pytest.mark.parametrize("bootstrap", [False, True])
def test_embedding_drift_preserves_the_callers_random_sequence(method, bootstrap):
    current, reference = _embeddings()
    np.random.seed(123)
    expected = np.random.RandomState(123).rand(5)

    method(bootstrap=bootstrap)(current, reference)

    np.testing.assert_array_equal(np.random.rand(5), expected)


@pytest.mark.parametrize("seed", [0, 17, 99])
def test_random_auc_keeps_its_seeded_values_without_changing_global_state(seed):
    labels = np.array([0, 1, 0, 0, 1, 1, 0, 1])
    expected_auc = roc_auc_score(labels, np.random.RandomState(seed).rand(len(labels)))
    np.random.seed(456)
    expected_sequence = np.random.RandomState(456).rand(5)

    actual_auc = calc_roc_auc_random(labels, seed)

    assert actual_auc == expected_auc
    np.testing.assert_array_equal(np.random.rand(5), expected_sequence)


@pytest.mark.parametrize("method", [distance, mmd, model])
def test_embedding_bootstrap_remains_independent_of_the_external_seed(method):
    np.random.seed(1)
    first = method(bootstrap=True)(*_embeddings())
    np.random.seed(987)
    second = method(bootstrap=True)(*_embeddings())

    assert first[0] == pytest.approx(second[0])
    assert first[1:] == second[1:]
