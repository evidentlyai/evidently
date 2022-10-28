from datetime import datetime

import numpy as np
import pandas as pd
import pytest

from evidently.analyzers.data_quality_analyzer import DataQualityAnalyzer
from evidently.dashboard.widgets.data_quality_features_widget import DataQualityFeaturesWidget
from evidently.model.widget import BaseWidgetInfo
from evidently.options import OptionsProvider
from evidently.pipeline.column_mapping import ColumnMapping


@pytest.fixture
def widget() -> DataQualityFeaturesWidget:
    options_provider = OptionsProvider()

    widget = DataQualityFeaturesWidget("test_data_quality_features_widget")
    widget.options_provider = options_provider
    return widget


def sample_data(feature1, feature2, feature3):
    return [
        {"feature1": t[0], "feature2": t[1], "feature3": t[2]}
        for t in zip(feature1, feature2, feature3)
    ]


@pytest.mark.parametrize(
    "reference, current, column_mapping",
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
def test_data_profile_widget_no_exceptions(reference, current, column_mapping):
    analyzer = DataQualityAnalyzer()
    analyzer.options_provider = OptionsProvider()
    results = analyzer.calculate(
        pd.DataFrame(reference), pd.DataFrame(current), column_mapping
    )

    widget = DataQualityFeaturesWidget("test")
    widget.options_provider = OptionsProvider()
    widget.calculate(
        pd.DataFrame(reference),
        pd.DataFrame(current),
        column_mapping,
        {
            DataQualityAnalyzer: results,
        },
    )


def test_data_profile_widget_regression_data():
    analyzer = DataQualityAnalyzer()
    reference_data = pd.DataFrame(
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
    widget.calculate(
        reference_data,
        reference_data,
        data_mapping,
        {
            DataQualityAnalyzer: results,
        },
    )


def test_data_quality_features_widget_analyzer_list(
    widget: DataQualityFeaturesWidget,
) -> None:
    assert widget.analyzers() == [DataQualityAnalyzer]


@pytest.mark.parametrize(
    "reference_data, current_data, data_mapping, expected_result",
    (
        (
            pd.DataFrame(
                {
                    "target": [1, 2, 3, 4],
                    "category_feature": ["test1", np.nan, None, ""],
                    "numerical_feature": [np.nan, 2, 2, 432],
                    "datetime_feature": [
                        pd.NaT,
                        datetime(year=2012, month=1, day=5),
                        datetime(year=2002, month=12, day=5, hour=12),
                        datetime(year=2012, month=1, day=5),
                    ],
                    "datetime": [
                        datetime(year=2022, month=1, day=1),
                        datetime(year=2022, month=1, day=2),
                        datetime(year=2022, month=12, day=3),
                        datetime(year=2022, month=1, day=4),
                    ],
                }
            ),
            None,
            ColumnMapping(datetime_features=["datetime_feature"], datetime="datetime"),
            BaseWidgetInfo(type="list", title="", size=2),
        ),
        (
            pd.DataFrame({"data": [1, 2, 3, 4]}),
            pd.DataFrame({"data": [1, 2, 3, 1]}),
            ColumnMapping(target=None),
            BaseWidgetInfo(type="list", title="", size=2),
        ),
    ),
)
def test_data_quality_features_widget(
    widget: DataQualityFeaturesWidget,
    reference_data: pd.DataFrame,
    current_data: pd.DataFrame,
    data_mapping: ColumnMapping,
    expected_result: BaseWidgetInfo,
) -> None:
    analyzer = DataQualityAnalyzer()
    analyzer.options_provider = widget.options_provider
    analyzer_results = analyzer.calculate(reference_data, current_data, data_mapping)
    result = widget.calculate(
        reference_data,
        current_data,
        data_mapping,
        {DataQualityAnalyzer: analyzer_results},
    )
    assert result.type == expected_result.type
    assert result.title == expected_result.title
    assert result.size == expected_result.size
    assert result.params is None
