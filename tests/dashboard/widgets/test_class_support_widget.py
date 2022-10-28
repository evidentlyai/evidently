import pandas as pd
import pytest

from evidently.analyzers.classification_performance_analyzer import ClassificationPerformanceAnalyzer
from evidently.dashboard.widgets.class_support_widget import ClassSupportWidget
from evidently.options import OptionsProvider
from evidently.pipeline.column_mapping import ColumnMapping


@pytest.fixture
def widget() -> ClassSupportWidget:
    options_provider = OptionsProvider()

    widget = ClassSupportWidget("test_widget")
    widget.options_provider = options_provider
    return widget


@pytest.mark.parametrize("dataset", ("reference", "current"))
def test_class_support_widget_simple_case(
    widget: ClassSupportWidget, dataset: str
) -> None:
    reference_data = pd.DataFrame(
        {
            "target": [1, 2, 3, 1],
            "prediction": [1, 2, 3, 2],
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
