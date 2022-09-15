import pytest
from evidently import ColumnMapping
from evidently.analyzers.data_drift_analyzer import DataDriftAnalyzer
from evidently.dashboard.widgets.data_drift_table_widget import DataDriftTableWidget
from evidently.options import OptionsProvider
from pandas import DataFrame


def sample_data(feature1, feature2, feature3):
    return [{"feature1": t[0], "feature2": t[1], "feature3": t[2]} for t in zip(feature1, feature2, feature3)]


@pytest.mark.parametrize(
    ["reference", "current", "column_mapping"],
    [
        (sample_data([1, 1], [1, 1], [1, 1]), sample_data([1, 1], [1, 1], [1, 1]), ColumnMapping()),
        (sample_data(["1", "1"], [1, 1], [1, 1]), sample_data(["1", "1"], [1, 1], [1, 1]), ColumnMapping()),
        (sample_data([True, True], [1, 1], [1, 1]), sample_data([True, True], [1, 1], [1, 1]), ColumnMapping()),
    ],
)
def test_data_drift_analyzer_no_exceptions(reference, current, column_mapping):
    analyzer = DataDriftAnalyzer()
    analyzer.options_provider = OptionsProvider()
    results = analyzer.calculate(DataFrame(reference), DataFrame(current), column_mapping)

    widget = DataDriftTableWidget("")
    widget.options_provider = OptionsProvider()
    widget.calculate(
        DataFrame(reference),
        DataFrame(current),
        column_mapping,
        {
            DataDriftAnalyzer: results,
        },
    )
