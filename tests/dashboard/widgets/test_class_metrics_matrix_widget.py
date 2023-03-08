import pandas as pd
import pytest

from evidently.analyzers.classification_performance_analyzer import (
    ClassificationPerformanceAnalyzer,
)
from evidently.dashboard.widgets.class_metrics_matrix_widget import (
    ClassMetricsMatrixWidget,
)
from evidently.options import OptionsProvider
from evidently.pipeline.column_mapping import ColumnMapping


@pytest.fixture
def widget() -> ClassMetricsMatrixWidget:
    options_provider = OptionsProvider()

    widget = ClassMetricsMatrixWidget("test_widget")
    widget.options_provider = options_provider
    return widget


@pytest.mark.parametrize("dataset", ("reference", "current"))
def test_class_quality_metrics_bar_widget_simple_case(
    widget: ClassMetricsMatrixWidget, dataset: str
) -> None:
    reference_data = pd.DataFrame(
        {
            "target": ["a", "b", "c"],
            "prediction": ["b", "a", "c"],
        }
    )
    analyzer = ClassificationPerformanceAnalyzer()
    analyzer.options_provider = widget.options_provider
    column_mapping = ColumnMapping()
    results = analyzer.calculate(reference_data, reference_data, column_mapping)

    widget.dataset = dataset
    assert widget.analyzers() == [ClassificationPerformanceAnalyzer]
    result = widget.calculate(
        reference_data,
        reference_data,
        column_mapping,
        {ClassificationPerformanceAnalyzer: results},
    )
    assert result is not None
    assert result.title == "test_widget"
    assert result.params is not None
