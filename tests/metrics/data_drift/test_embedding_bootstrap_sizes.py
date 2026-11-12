import numpy as np
import pandas as pd
import pytest

from evidently import DataDefinition
from evidently import Dataset
from evidently import Report
from evidently.legacy.metrics.data_drift.embedding_drift_methods import DistanceDriftMethod
from evidently.legacy.metrics.data_drift.embedding_drift_methods import MMDDriftMethod
from evidently.metrics import EmbeddingsDrift


@pytest.fixture(autouse=True)
def restore_random_state():
    state = np.random.get_state()
    yield
    np.random.set_state(state)


def distance_reference(reference, current, bootstrap):
    score = np.linalg.norm(reference.mean(axis=0) - current.mean(axis=0))
    threshold = 0.2
    if bootstrap:
        sizes = np.array([len(reference), len(current)])
        counts = np.maximum(sizes * len(reference) // sizes.sum(), 1)
        distances = []
        for seed in range(100):
            rng = np.random.RandomState(seed)
            left = reference[rng.choice(len(reference), counts[0])]
            right = reference[rng.choice(len(reference), counts[1])]
            distances.append(np.linalg.norm(left.mean(axis=0) - right.mean(axis=0)))
        threshold = np.percentile(distances, 95)
    return score, score > threshold


def rbf_kernel(left, right, bandwidth):
    distances = np.linalg.norm(left[:, None] - right[None, :], axis=-1)
    return np.exp(-np.square(distances / bandwidth))


def unbiased_mmd(left, right, bandwidth):
    within_left = rbf_kernel(left, left, bandwidth)
    within_right = rbf_kernel(right, right, bandwidth)
    return (
        within_left[~np.eye(len(left), dtype=bool)].mean()
        + within_right[~np.eye(len(right), dtype=bool)].mean()
        - 2 * rbf_kernel(left, right, bandwidth).mean()
    )


def mmd_reference(reference, current, bootstrap):
    bandwidth = np.median(np.linalg.norm(reference[:, None] - current[None, :], axis=-1))
    score = unbiased_mmd(reference, current, bandwidth)
    threshold = 0.015
    if bootstrap:
        bandwidth = np.median(np.linalg.norm(reference[:, None] - reference[None, :], axis=-1))
        sizes = np.array([len(reference), len(current)])
        counts = np.maximum(sizes * len(reference) // sizes.sum(), 2)
        statistics = []
        for seed in range(100):
            rng = np.random.RandomState(seed)
            left = reference[rng.choice(len(reference), counts[0])]
            right = reference[rng.choice(len(reference), counts[1])]
            statistics.append(unbiased_mmd(left, right, bandwidth))
        threshold = np.percentile(statistics, 95)
    return max(score, 0), score > threshold


@pytest.mark.parametrize("bootstrap", [False, True])
@pytest.mark.parametrize("sizes", [(1, 8), (2, 8), (3, 9), (10, 3), (8, 8)])
def test_distance_bootstrap_keeps_both_sample_means_defined(sizes, bootstrap):
    reference = np.arange(sizes[0], dtype=float)[:, None]
    current = np.arange(sizes[1], dtype=float)[:, None] + 30
    expected_score, expected_drift = distance_reference(reference, current, bootstrap)

    score, drifted, method = DistanceDriftMethod(bootstrap=bootstrap)(pd.DataFrame(current), pd.DataFrame(reference))

    assert score == pytest.approx(expected_score)
    assert drifted == expected_drift
    assert method == "distance"


@pytest.mark.parametrize("reference_size", [1, 3])
def test_cityblock_drift_does_not_compare_against_a_nan_bootstrap_threshold(reference_size):
    reference = pd.DataFrame({"x": np.arange(reference_size, dtype=float)})
    current = pd.DataFrame({"x": np.arange(12, dtype=float) + 30})

    score, drifted, _ = DistanceDriftMethod(dist="cityblock", bootstrap=True)(current, reference)

    assert score > 30
    assert drifted


@pytest.mark.parametrize("bootstrap", [False, True])
@pytest.mark.parametrize("sizes", [(2, 2), (2, 8), (3, 9), (10, 3), (8, 8)])
def test_mmd_bootstrap_keeps_two_observations_in_each_subsample(sizes, bootstrap):
    reference = np.arange(sizes[0], dtype=float)[:, None]
    current = np.arange(sizes[1], dtype=float)[:, None] + 3.5
    expected_score, expected_drift = mmd_reference(reference, current, bootstrap)

    score, drifted, method = MMDDriftMethod(bootstrap=bootstrap, quantile_probability=0.95)(
        pd.DataFrame(current), pd.DataFrame(reference)
    )

    assert score == pytest.approx(expected_score, abs=1e-12)
    assert drifted == expected_drift
    assert method == "mmd"


@pytest.mark.parametrize(
    "method_type,current_size,reference_function",
    [(DistanceDriftMethod, 500, distance_reference), (MMDDriftMethod, 200, mmd_reference)],
)
def test_embedding_report_supports_imbalanced_bootstrap_populations(method_type, current_size, reference_function):
    rng = np.random.RandomState(12)
    reference = rng.normal(size=(20, 2))
    current = rng.normal(2, size=(current_size, 2))
    expected_score, _ = reference_function(reference, current, True)
    definition = DataDefinition(embeddings={"embedding": ["x", "y"]})
    reference_data = Dataset.from_pandas(pd.DataFrame(reference, columns=["x", "y"]), definition)
    current_data = Dataset.from_pandas(pd.DataFrame(current, columns=["x", "y"]), definition)
    method = method_type(bootstrap=True, quantile_probability=0.95)

    snapshot = Report(metrics=[EmbeddingsDrift(embeddings_name="embedding", drift_method=method)]).run(
        current_data, reference_data
    )

    result = next(iter(snapshot.metric_results.values()))
    assert result.value == pytest.approx(expected_score)
