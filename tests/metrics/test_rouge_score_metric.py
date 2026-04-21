"""Tests for RougeScoreMetric (dataset-level aggregate)."""

import pandas as pd
import pytest

from evidently.core.datasets import Dataset
from evidently.core.datasets import DataDefinition
from evidently.metrics.text_evals import RougeScoreMetric

rouge_score = pytest.importorskip("rouge_score", reason="rouge-score not installed; run pip install evidently[llm]")


def _make_dataset(data: dict) -> Dataset:
    df = pd.DataFrame(data)
    return Dataset.from_pandas(df, data_definition=DataDefinition())


SAMPLE_DATA = {
    "pred": [
        "the cat sat on the mat",
        "machine learning is fascinating",
        "hello world",
        "the quick brown fox",
    ],
    "ref": [
        "the cat sat on the mat",
        "artificial intelligence is interesting",
        "goodbye universe",
        "the quick brown fox jumps over the lazy dog",
    ],
}


def test_rouge_score_metric_returns_value_in_range():
    from evidently.metrics.text_evals import RougeScoreMetricCalculation

    metric = RougeScoreMetric(prediction_column="pred", reference_column="ref", rouge_type="rouge1")
    ds = _make_dataset(SAMPLE_DATA)
    calc = RougeScoreMetricCalculation(metric_id="test", metric=metric)
    cur, ref = calc.calculate(context=None, current_data=ds, reference_data=None)  # type: ignore[arg-type]

    assert 0.0 <= cur.value <= 1.0
    assert ref is None


def test_rouge_score_metric_with_reference():
    from evidently.metrics.text_evals import RougeScoreMetricCalculation

    metric = RougeScoreMetric(prediction_column="pred", reference_column="ref", rouge_type="rouge1")
    current = _make_dataset(SAMPLE_DATA)
    reference = _make_dataset(
        {
            "pred": ["identical text identical text", "completely different here"],
            "ref": ["identical text identical text", "nothing matches at all"],
        }
    )
    calc = RougeScoreMetricCalculation(metric_id="test", metric=metric)
    cur, ref = calc.calculate(context=None, current_data=current, reference_data=reference)  # type: ignore[arg-type]

    assert 0.0 <= cur.value <= 1.0
    assert ref is not None
    assert 0.0 <= ref.value <= 1.0


def test_rouge_score_metric_identical_texts_score_one():
    """If all predictions exactly match references, mean ROUGE-1 should be 1.0."""
    from evidently.metrics.text_evals import RougeScoreMetricCalculation

    metric = RougeScoreMetric(prediction_column="pred", reference_column="ref", rouge_type="rouge1")
    ds = _make_dataset(
        {
            "pred": ["the cat sat on the mat", "hello world"],
            "ref": ["the cat sat on the mat", "hello world"],
        }
    )
    calc = RougeScoreMetricCalculation(metric_id="test", metric=metric)
    cur, _ = calc.calculate(context=None, current_data=ds, reference_data=None)  # type: ignore[arg-type]
    assert cur.value == pytest.approx(1.0, abs=1e-6)


def test_rouge_score_metric_rouge2():
    from evidently.metrics.text_evals import RougeScoreMetricCalculation

    metric = RougeScoreMetric(prediction_column="pred", reference_column="ref", rouge_type="rouge2", score_type="f")
    ds = _make_dataset(SAMPLE_DATA)
    calc = RougeScoreMetricCalculation(metric_id="test", metric=metric)
    cur, _ = calc.calculate(context=None, current_data=ds, reference_data=None)  # type: ignore[arg-type]
    assert 0.0 <= cur.value <= 1.0


def test_rouge_score_metric_rougeL():
    from evidently.metrics.text_evals import RougeScoreMetricCalculation

    metric = RougeScoreMetric(prediction_column="pred", reference_column="ref", rouge_type="rougeL", score_type="f")
    ds = _make_dataset(SAMPLE_DATA)
    calc = RougeScoreMetricCalculation(metric_id="test", metric=metric)
    cur, _ = calc.calculate(context=None, current_data=ds, reference_data=None)  # type: ignore[arg-type]
    assert 0.0 <= cur.value <= 1.0


def test_rouge_score_metric_precision_and_recall():
    from evidently.metrics.text_evals import RougeScoreMetricCalculation

    ds = _make_dataset(SAMPLE_DATA)
    for score_type in ("precision", "recall"):
        metric = RougeScoreMetric(
            prediction_column="pred", reference_column="ref", rouge_type="rouge1", score_type=score_type
        )
        calc = RougeScoreMetricCalculation(metric_id="test", metric=metric)
        cur, _ = calc.calculate(context=None, current_data=ds, reference_data=None)  # type: ignore[arg-type]
        assert 0.0 <= cur.value <= 1.0, f"score_type={score_type} gave {cur.value}"


def test_rouge_score_metric_invalid_rouge_type():
    from evidently.metrics.text_evals import RougeScoreMetricCalculation

    metric = RougeScoreMetric(prediction_column="pred", reference_column="ref", rouge_type="rouge99")
    ds = _make_dataset(SAMPLE_DATA)
    calc = RougeScoreMetricCalculation(metric_id="test", metric=metric)
    with pytest.raises(ValueError, match="rouge_type"):
        calc.calculate(context=None, current_data=ds, reference_data=None)  # type: ignore[arg-type]


def test_rouge_score_metric_display_name():
    from evidently.metrics.text_evals import RougeScoreMetricCalculation

    metric = RougeScoreMetric(prediction_column="pred", reference_column="ref", rouge_type="rouge1", score_type="f")
    calc = RougeScoreMetricCalculation(metric_id="test", metric=metric)
    name = calc.display_name()
    assert "ROUGE1" in name
    assert "pred" in name
    assert "ref" in name
