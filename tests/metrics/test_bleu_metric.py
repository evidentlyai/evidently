import pytest
import pandas as pd
from evidently.metrics.bleu_metric import BLEUMetric

def test_bleu_metric():
    data = pd.DataFrame({
        "reference": ["the cat is on the mat", "there is a cat on the mat"],
        "hypothesis": ["the cat is on the mat", "there is cat on mat"]
    })
    metric = BLEUMetric(reference_column="reference", hypothesis_column="hypothesis")
    result = metric.calculate(data)
    assert result.average_bleu_score == pytest.approx(0.7598356856515925, rel=1e-2)
    assert len(result.bleu_scores) == 2
    assert result.bleu_scores[0] == pytest.approx(1.0, rel=1e-2)
    assert result.bleu_scores[1] == pytest.approx(0.519671371303185, rel=1e-2)
