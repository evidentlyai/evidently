import pytest
from pandas import DataFrame
from pytest import approx

from evidently import ColumnMapping
from evidently.analyzers.classification_performance_analyzer import ClassificationPerformanceAnalyzer


@pytest.fixture
def analyzer() -> ClassificationPerformanceAnalyzer:
    return ClassificationPerformanceAnalyzer()


def test_different_column_names(analyzer: ClassificationPerformanceAnalyzer) -> None:
    reference_data = DataFrame({
        'target': [1, 0, 1, 1, 0, 1],
        'prediction': [1, 1, 0, 1, 0, 1],
    })
    current_data = DataFrame({
        'target': [1, 0, 1, 1, 0, 1, 5, 1, 4, 1, 0],
        'prediction': [1, 1, 0, 1, 0, 1, 4, 12, 0, 1, 0],
    })

    result = analyzer.calculate(reference_data, current_data, column_mapping=ColumnMapping())
    assert result.columns is not None
    assert result.columns.target_names is None
    assert result.reference_metrics is not None
    assert result.reference_metrics.accuracy == approx(2 / 3)
    assert result.reference_metrics.precision == 0.625
    assert result.reference_metrics.recall == 0.625
    assert result.reference_metrics.f1 == 0.625
    assert isinstance(result.reference_metrics.metrics_matrix, dict)
    assert result.reference_metrics.metrics_matrix

    assert result.current_metrics is not None
    assert result.current_metrics.accuracy == approx(0.54545, 1e-5)
    assert result.current_metrics.precision == 0.26
    assert result.current_metrics.recall == approx(0.2667, 1e-3)
    assert result.current_metrics.f1 == approx(0.25974, 1e-4)
    assert isinstance(result.current_metrics.metrics_matrix, dict)
    assert result.current_metrics.metrics_matrix
