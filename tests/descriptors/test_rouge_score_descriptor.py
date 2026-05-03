"""Tests for the RougeScore Descriptor."""

import pandas as pd
import pytest

from evidently.core.datasets import Dataset
from evidently.core.datasets import DataDefinition
from evidently.descriptors import RougeScore

rouge_score = pytest.importorskip("rouge_score", reason="rouge-score not installed; run pip install evidently[llm]")


def _make_dataset(data: dict) -> Dataset:
    df = pd.DataFrame(data)
    return Dataset.from_pandas(df, data_definition=DataDefinition())


def test_rouge_score_descriptor_basic():
    """Descriptor should add a numeric column in [0, 1] to the dataset."""
    ds = _make_dataset(
        {
            "pred": ["the cat sat on the mat", "hello world"],
            "ref": ["the cat sat on the mat", "goodbye moon"],
        }
    )
    desc = RougeScore("pred", "ref", rouge_type="rouge1")
    result = desc.generate_data(ds, options=None)  # type: ignore[arg-type]

    assert result.type.value == "num"
    scores = result.data.tolist()
    assert len(scores) == 2
    assert scores[0] == pytest.approx(1.0, abs=1e-6)
    assert 0.0 <= scores[1] <= 1.0


def test_rouge_score_descriptor_rouge2():
    ds = _make_dataset(
        {
            "output": ["the quick brown fox jumps over", "completely different words"],
            "ground_truth": ["the quick brown fox jumps", "nothing in common here at all"],
        }
    )
    desc = RougeScore("output", "ground_truth", rouge_type="rouge2", score_type="f")
    result = desc.generate_data(ds, options=None)  # type: ignore[arg-type]
    scores = result.data.tolist()
    assert all(0.0 <= s <= 1.0 for s in scores)
    # first pair has bigram overlap; should score > 0
    assert scores[0] > 0.0


def test_rouge_score_descriptor_rougeL():
    ds = _make_dataset(
        {
            "pred": ["the cat sat on the mat"],
            "ref": ["the cat sat on the mat"],
        }
    )
    desc = RougeScore("pred", "ref", rouge_type="rougeL", score_type="f")
    result = desc.generate_data(ds, options=None)  # type: ignore[arg-type]
    assert result.data.iloc[0] == pytest.approx(1.0, abs=1e-6)


def test_rouge_score_descriptor_precision_and_recall():
    ds = _make_dataset(
        {
            "pred": ["the cat sat on the mat"],
            "ref": ["the cat sat"],
        }
    )
    # Prediction is a superset → high recall on ref, lower precision
    precision_desc = RougeScore("pred", "ref", rouge_type="rouge1", score_type="precision")
    recall_desc = RougeScore("pred", "ref", rouge_type="rouge1", score_type="recall")

    precision_score = precision_desc.generate_data(ds, options=None).data.iloc[0]  # type: ignore[arg-type]
    recall_score = recall_desc.generate_data(ds, options=None).data.iloc[0]  # type: ignore[arg-type]

    assert 0.0 <= precision_score <= 1.0
    assert 0.0 <= recall_score <= 1.0
    # All ref words are in pred → recall should be 1.0
    assert recall_score == pytest.approx(1.0, abs=1e-6)


def test_rouge_score_descriptor_nan_handling():
    ds = _make_dataset(
        {
            "pred": [None, "hello world"],
            "ref": ["some text", None],
        }
    )
    desc = RougeScore("pred", "ref", rouge_type="rouge1")
    result = desc.generate_data(ds, options=None)  # type: ignore[arg-type]
    assert len(result.data) == 2
    assert all(0.0 <= s <= 1.0 for s in result.data.tolist())


def test_rouge_score_descriptor_alias():
    desc = RougeScore("pred", "ref", rouge_type="rouge1", alias="My ROUGE")
    assert desc.alias == "My ROUGE"


def test_rouge_score_descriptor_default_alias():
    desc = RougeScore("pred", "ref", rouge_type="rouge1", score_type="f")
    assert "rouge1" in desc.alias
    assert "f" in desc.alias


def test_rouge_score_descriptor_list_input_columns():
    desc = RougeScore("prediction", "reference")
    assert desc.list_input_columns() == ["prediction", "reference"]


def test_rouge_score_descriptor_invalid_rouge_type():
    with pytest.raises(ValueError, match="rouge_type"):
        RougeScore("pred", "ref", rouge_type="rouge99")


def test_rouge_score_descriptor_invalid_score_type():
    with pytest.raises(ValueError, match="score_type"):
        RougeScore("pred", "ref", score_type="unknown")
