from datetime import datetime

import pytest
from pandas import DataFrame

from evidently import ColumnMapping
from evidently.analyzers.data_quality_analyzer import DataQualityAnalyzer
from evidently.dashboard.widgets.data_profile_features_widget import DataQualityFeaturesWidget
from evidently.options import OptionsProvider


def sample_data(feature1, feature2, feature3):
    return [{'feature1': t[0], 'feature2': t[1], 'feature3': t[2]} for t in zip(feature1, feature2, feature3)]


@pytest.mark.parametrize(
    "reference, current, column_mapping",
    [
        (sample_data([1, 1], [1, 1], [1, 1]), sample_data([1, 1], [1, 1], [1, 1]), ColumnMapping()),
        (sample_data(["1", "1"], [1, 1], [1, 1]), sample_data(["1", "1"], [1, 1], [1, 1]), ColumnMapping()),
        (sample_data([True, True], [1, 1], [1, 1]), sample_data([True, True], [1, 1], [1, 1]), ColumnMapping()),
    ])
def test_data_profile_widget_no_exceptions(reference, current, column_mapping):
    analyzer = DataQualityAnalyzer()
    analyzer.options_provider = OptionsProvider()
    results = analyzer.calculate(DataFrame(reference), DataFrame(current), column_mapping)

    widget = DataQualityFeaturesWidget("test")
    widget.options_provider = OptionsProvider()
    widget.calculate(DataFrame(reference), DataFrame(current), column_mapping, {
        DataQualityAnalyzer: results,
    })


def test_data_profile_widget_regression_data():
    analyzer = DataQualityAnalyzer()
    reference_data = DataFrame(
        {
            "target": [1, 2, 3, 1],
            "numerical_feature_1": [0, 2, -1, 5],
            "numerical_feature_2": [0.3, 5, 0.3, 3.4],
            "categorical_feature_1": [1, 1, 5, None],
            "categorical_feature_2": ["y", "y", "n", "n"],
            "datetime_feature_1": [
                datetime(year=2022, month=2, day=22),
                datetime(year=2021, month=3, day=2),
                datetime(year=2022, month=12, day=31),
                datetime(year=2022, month=2, day=22),
            ],
        }
    )
    data_mapping = ColumnMapping(
        numerical_features=["numerical_feature_1", "numerical_feature_2"],
        categorical_features=["categorical_feature_1", "categorical_feature_2"],
        datetime_features=["datetime_feature_1"],
        task="regression",
    )

    results = analyzer.calculate(reference_data, reference_data, data_mapping)

    widget = DataQualityFeaturesWidget("test")
    widget.options_provider = OptionsProvider()
    widget.calculate(reference_data, reference_data, data_mapping, {
        DataQualityAnalyzer: results,
    })
