from datetime import datetime

import numpy as np
import pandas as pd

import pytest

from evidently.analyzers.data_quality_analyzer import DataQualityAnalyzer
from evidently.model.widget import BaseWidgetInfo
from evidently.options import OptionsProvider
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.dashboard.widgets.data_quality_correlations import DataQualityCorrelationsWidget


@pytest.fixture
def widget() -> DataQualityCorrelationsWidget:
    options_provider = OptionsProvider()

    widget = DataQualityCorrelationsWidget("test_data_quality_correlations_widget")
    widget.options_provider = options_provider
    return widget


def test_test_data_quality_correlations_widget_analyzer_list(widget: DataQualityCorrelationsWidget) -> None:
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
            BaseWidgetInfo(type="rich_data", title="", size=2),
        ),
        (
            pd.DataFrame({"data": [1, 2, 3, 4]}),
            pd.DataFrame({"data": [1, 2, 3, 1]}),
            ColumnMapping(target=None),
            BaseWidgetInfo(type="rich_data", title="", size=2),
        ),
    ),
)
def test_data_quality_features_widget(
    widget: DataQualityCorrelationsWidget,
    reference_data: pd.DataFrame,
    current_data: pd.DataFrame,
    data_mapping: ColumnMapping,
    expected_result: BaseWidgetInfo,
) -> None:
    analyzer = DataQualityAnalyzer()
    analyzer.options_provider = widget.options_provider
    analyzer_results = analyzer.calculate(reference_data, current_data, data_mapping)
    result = widget.calculate(reference_data, current_data, data_mapping, {DataQualityAnalyzer: analyzer_results})
    assert result.type == expected_result.type
    assert result.title == expected_result.title
    assert result.size == expected_result.size
    assert result.params is not None
