import numpy as np
import pandas as pd
import pytest
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split

from evidently import DataDefinition
from evidently import Dataset
from evidently import Report
from evidently.legacy.metrics.data_drift.embedding_drift_methods import ModelDriftMethod
from evidently.metrics import EmbeddingsDrift


@pytest.fixture(autouse=True)
def restore_random_state():
    state = np.random.get_state()
    yield
    np.random.set_state(state)


@pytest.mark.parametrize("sizes", [(2, 8), (8, 2), (3, 4), (10, 10)])
@pytest.mark.parametrize("bootstrap", [False, True])
def test_model_drift_keeps_both_populations_in_each_split(sizes, bootstrap):
    reference_size, current_size = sizes
    reference = pd.DataFrame({"embedding": np.arange(reference_size) * 0.01 - 10})
    current = pd.DataFrame({"embedding": np.arange(current_size) * 0.01 + 10})
    labels = np.r_[np.ones(reference_size), np.zeros(current_size)]
    _, expected_labels = train_test_split(labels, test_size=0.5, random_state=42, stratify=labels)
    threshold = 0.55
    if bootstrap:
        threshold = np.percentile(
            [roc_auc_score(expected_labels, np.random.RandomState(i).rand(len(expected_labels))) for i in range(100)],
            95,
        )

    score, drifted, method = ModelDriftMethod(bootstrap=bootstrap)(current, reference)

    assert score == 1.0
    assert drifted == (score > threshold)
    assert method == "model"


def test_model_drift_matches_a_stratified_classifier_reference():
    rng = np.random.RandomState(16)
    reference = pd.DataFrame(rng.normal(size=(17, 3)), columns=["x", "y", "z"])
    current = pd.DataFrame(rng.normal(0.2, size=(9, 3)), columns=["x", "y", "z"])
    data = pd.concat([reference, current])
    labels = np.r_[np.ones(len(reference)), np.zeros(len(current))]
    x_train, x_test, y_train, y_test = train_test_split(
        data, labels, test_size=0.5, random_state=42, shuffle=True, stratify=labels
    )
    classifier = SGDClassifier(loss="log_loss", random_state=42).fit(x_train, y_train)
    expected = roc_auc_score(y_test, classifier.predict_proba(x_test)[:, 1])

    actual = ModelDriftMethod()(current, reference)

    assert actual == (expected, expected > 0.55, "model")


def test_model_drift_report_keeps_imbalanced_populations_supported():
    definition = DataDefinition(embeddings={"embedding": ["x", "y"]})
    reference = Dataset.from_pandas(
        pd.DataFrame({"x": [-10.0, -9.9, -10.2, -9.8], "y": [-5.0, -5.3, -4.8, -5.1]}), definition
    )
    current = Dataset.from_pandas(pd.DataFrame({"x": np.arange(31) + 10, "y": np.arange(31) % 7 + 5}), definition)
    metric = EmbeddingsDrift(embeddings_name="embedding", drift_method=ModelDriftMethod())

    snapshot = Report(metrics=[metric]).run(current, reference)

    result = next(iter(snapshot.metric_results.values()))
    assert result.value == 1.0
