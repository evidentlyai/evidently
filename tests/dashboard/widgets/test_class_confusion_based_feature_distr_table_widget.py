import pandas as pd

from evidently.analyzers.classification_performance_analyzer import ClassificationPerformanceAnalyzer
from evidently.dashboard.widgets.class_confusion_based_feature_distr_table_widget import \
    ClassConfusionBasedFeatureDistrTable
from evidently.options import OptionsProvider
from evidently.pipeline.column_mapping import ColumnMapping

import pytest


@pytest.fixture
def widget() -> ClassConfusionBasedFeatureDistrTable:
    options_provider = OptionsProvider()

    widget = ClassConfusionBasedFeatureDistrTable("test_widget")
    widget.options_provider = options_provider
    return widget


def test_class_confusion_based_feature_distr_table_simple_case(
        widget: ClassConfusionBasedFeatureDistrTable
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

    assert widget.analyzers() == [ClassificationPerformanceAnalyzer]
    result = widget.calculate(reference_data, None, column_mapping, {ClassificationPerformanceAnalyzer: results})
    assert result is not None
    assert result.title == "test_widget"
    assert result.params is not None
