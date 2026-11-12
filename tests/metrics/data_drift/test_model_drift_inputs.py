import numpy as np
import pandas as pd
import pytest

from evidently.legacy.metrics.data_drift.embedding_drift_methods import ModelDriftMethod
from evidently.legacy.metrics.data_drift.embedding_drift_methods import model


def embeddings():
    rng = np.random.RandomState(42)
    reference = pd.DataFrame({"noise": rng.normal(size=40), "target": rng.normal(-5, 0.1, 40)})
    current = pd.DataFrame({"noise": rng.normal(size=40), "target": rng.normal(5, 0.1, 40)})
    return current, reference


@pytest.mark.parametrize("bootstrap", [False, True])
@pytest.mark.parametrize("pca_components", [None, 2])
def test_model_drift_preserves_input_embeddings(bootstrap, pca_components):
    current, reference = embeddings()
    original_current, original_reference = current.copy(), reference.copy()

    model(bootstrap=bootstrap, pca_components=pca_components)(current, reference)

    pd.testing.assert_frame_equal(current, original_current)
    pd.testing.assert_frame_equal(reference, original_reference)


@pytest.mark.parametrize("pca_components", [None, 2])
def test_model_drift_uses_embedding_dimension_named_target(pca_components):
    current, reference = embeddings()
    renamed_current = current.rename(columns={"target": "signal"})
    renamed_reference = reference.rename(columns={"target": "signal"})
    method = ModelDriftMethod(pca_components=pca_components)

    expected = method(renamed_current, renamed_reference)
    actual = method(current, reference)

    assert expected == (1.0, True, "model")
    assert actual == expected


def test_model_drift_accepts_the_same_dataframe_as_both_samples():
    sample = pd.DataFrame({"first": np.zeros(20), "second": np.zeros(20)})

    assert model()(sample, sample) == (0.5, False, "model")
    assert list(sample.columns) == ["first", "second"]
