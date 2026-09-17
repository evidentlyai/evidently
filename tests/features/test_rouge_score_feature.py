"""Tests for RougeScoreFeature (legacy feature layer)."""

import pandas as pd
import pytest

from evidently.legacy.features.rouge_score_feature import RougeScoreFeature
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.utils.data_preprocessing import create_data_definition

rouge_score = pytest.importorskip("rouge_score", reason="rouge-score not installed; run pip install evidently[llm]")


@pytest.mark.parametrize(
    "prediction, reference, rouge_type, score_type, expected_range",
    [
        # Identical texts → perfect score
        ("the cat sat on the mat", "the cat sat on the mat", "rouge1", "f", (0.99, 1.01)),
        # Completely different → near zero
        ("apple orange banana", "car train airplane", "rouge1", "f", (0.0, 0.1)),
        # Partial overlap — rouge1 F1
        ("the cat sat", "the cat sat on the mat", "rouge1", "f", (0.6, 0.9)),
        # Bigram overlap — rouge2 stricter than rouge1
        ("the quick brown fox", "the quick brown fox jumps", "rouge2", "f", (0.5, 1.0)),
        # rougeL on similar sentences
        ("machine learning is powerful", "machine learning is great", "rougeL", "f", (0.5, 1.0)),
        # score_type = precision
        ("cat sat mat", "the cat sat on the mat", "rouge1", "precision", (0.5, 1.01)),
        # score_type = recall
        ("the cat sat on the mat", "the cat sat", "rouge1", "recall", (0.5, 1.01)),
    ],
)
def test_rouge_score_feature_range(prediction, reference, rouge_type, score_type, expected_range):
    feature = RougeScoreFeature(
        columns=["prediction", "reference"],
        rouge_type=rouge_type,
        score_type=score_type,
    )
    data = pd.DataFrame({"prediction": [prediction], "reference": [reference]})
    result = feature.generate_feature(
        data=data,
        data_definition=create_data_definition(None, data, ColumnMapping()),
    )
    score = result[feature._feature_name()].iloc[0]
    assert expected_range[0] <= score <= expected_range[1], (
        f"Expected score in {expected_range}, got {score:.4f} "
        f"for rouge_type={rouge_type}, score_type={score_type}"
    )


def test_rouge_score_feature_empty_strings():
    """Empty strings should return 0, not raise an error."""
    feature = RougeScoreFeature(columns=["prediction", "reference"], rouge_type="rouge1", score_type="f")
    data = pd.DataFrame({"prediction": [""], "reference": [""]})
    result = feature.generate_feature(
        data=data,
        data_definition=create_data_definition(None, data, ColumnMapping()),
    )
    score = result[feature._feature_name()].iloc[0]
    assert score == 0.0


def test_rouge_score_feature_nan_handling():
    """NaN values should be treated as empty strings without raising."""
    feature = RougeScoreFeature(columns=["prediction", "reference"], rouge_type="rouge1", score_type="f")
    data = pd.DataFrame({"prediction": [None, "hello world"], "reference": ["some text", None]})
    result = feature.generate_feature(
        data=data,
        data_definition=create_data_definition(None, data, ColumnMapping()),
    )
    assert len(result) == 2
    assert all(0.0 <= v <= 1.0 for v in result[feature._feature_name()])


def test_rouge_score_feature_batch():
    """Multiple rows should each get their own score."""
    feature = RougeScoreFeature(columns=["pred", "ref"], rouge_type="rouge1", score_type="f")
    data = pd.DataFrame(
        {
            "pred": ["the cat sat", "hello world", "identical text"],
            "ref": ["the cat sat on the mat", "goodbye universe", "identical text"],
        }
    )
    result = feature.generate_feature(
        data=data,
        data_definition=create_data_definition(None, data, ColumnMapping()),
    )
    scores = result[feature._feature_name()].tolist()
    assert len(scores) == 3
    # last row is identical → score 1.0
    assert scores[2] == pytest.approx(1.0, abs=1e-6)
    # first two rows differ → lower scores
    assert scores[0] < 1.0
    assert scores[1] < 0.5


def test_rouge_score_feature_invalid_rouge_type():
    feature = RougeScoreFeature(columns=["pred", "ref"], rouge_type="rouge99", score_type="f")
    data = pd.DataFrame({"pred": ["text"], "ref": ["text"]})
    with pytest.raises(ValueError, match="rouge_type"):
        feature.generate_feature(
            data=data,
            data_definition=create_data_definition(None, data, ColumnMapping()),
        )


def test_rouge_score_feature_invalid_score_type():
    feature = RougeScoreFeature(columns=["pred", "ref"], rouge_type="rouge1", score_type="unknown")
    data = pd.DataFrame({"pred": ["text"], "ref": ["text"]})
    with pytest.raises(ValueError, match="score_type"):
        feature.generate_feature(
            data=data,
            data_definition=create_data_definition(None, data, ColumnMapping()),
        )


def test_rouge_score_feature_name():
    feature = RougeScoreFeature(columns=["pred", "ref"], rouge_type="rouge2", score_type="recall")
    assert feature._feature_name() == "pred|ref|rouge2|recall"
