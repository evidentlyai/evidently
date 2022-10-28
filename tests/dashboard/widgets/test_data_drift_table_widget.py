from datetime import datetime

import pandas as pd
import pytest

from evidently import ColumnMapping
from evidently.analyzers.data_drift_analyzer import DataDriftAnalyzer
from evidently.dashboard.widgets.data_drift_table_widget import DataDriftTableWidget
from evidently.options import OptionsProvider


def sample_data(feature1, feature2, feature3):
    return [
        {"feature1": t[0], "feature2": t[1], "feature3": t[2]}
        for t in zip(feature1, feature2, feature3)
    ]


@pytest.mark.parametrize(
    ["reference", "current", "column_mapping"],
    [
        (
            sample_data([1, 1], [1, 1], [1, 1]),
            sample_data([1, 1], [1, 1], [1, 1]),
            ColumnMapping(),
        ),
        (
            sample_data(["1", "1"], [1, 1], [1, 1]),
            sample_data(["1", "1"], [1, 1], [1, 1]),
            ColumnMapping(),
        ),
        (
            sample_data([True, True], [1, 1], [1, 1]),
            sample_data([True, True], [1, 1], [1, 1]),
            ColumnMapping(),
        ),
    ],
)
def test_data_drift_table_widget_no_exceptions(reference, current, column_mapping):
    analyzer = DataDriftAnalyzer()
    analyzer.options_provider = OptionsProvider()
    reference_data = pd.DataFrame(reference)
    current_data = pd.DataFrame(current)
    results = analyzer.calculate(reference_data, current_data, column_mapping)

    widget = DataDriftTableWidget("")
    widget.options_provider = OptionsProvider()
    widget.calculate(
        reference_data,
        current_data,
        column_mapping,
        {
            DataDriftAnalyzer: results,
        },
    )


def test_test_data_drift_table_widget_with_date_column():
    analyzer = DataDriftAnalyzer()
    analyzer.options_provider = OptionsProvider()
    data = pd.DataFrame(
        {
            "target": [2, 3, 4, 5, 6] * 200,
            "datetime": [
                datetime(year=3000 - i, month=1, day=5) for i in range(0, 1000)
            ],
        }
    )
    column_mapping = ColumnMapping(datetime="datetime")
    reference_data = data[:120]
    current_data = data[120:]
    results = analyzer.calculate(reference_data, current_data, ColumnMapping())

    widget = DataDriftTableWidget("")
    widget.options_provider = OptionsProvider()
    widget.calculate(
        reference_data,
        current_data,
        column_mapping,
        {
            DataDriftAnalyzer: results,
        },
    )
