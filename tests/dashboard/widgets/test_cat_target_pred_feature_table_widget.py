import pandas as pd
import pytest

from evidently.analyzers.cat_target_drift_analyzer import CatTargetDriftAnalyzer
from evidently.dashboard.widgets.cat_target_pred_feature_table_widget import (
    CatTargetPredFeatureTable,
)
from evidently.model.widget import BaseWidgetInfo
from evidently.options import OptionsProvider
from evidently.pipeline.column_mapping import ColumnMapping


@pytest.fixture
def widget() -> CatTargetPredFeatureTable:
    options_provider = OptionsProvider()
    widget = CatTargetPredFeatureTable("test_widget")
    widget.options_provider = options_provider
    return widget


def test_cat_target_pred_feature_table_widget_analyzer_list(
    widget: CatTargetPredFeatureTable,
) -> None:
    assert widget.analyzers() == [CatTargetDriftAnalyzer]


@pytest.mark.parametrize(
    "reference_data, current_data, data_mapping, expected_result",
    (
        (
            pd.DataFrame({"target": [1, 2, 3, 4]}),
            pd.DataFrame({"target": [1, 2, 3, 1]}),
            ColumnMapping(),
            BaseWidgetInfo(type="big_table", title="test_widget", size=2),
        ),
        (
            pd.DataFrame({"prediction": [1, 2, 3, 4]}),
            pd.DataFrame({"prediction": [1, 2, 3, 1]}),
            ColumnMapping(),
            BaseWidgetInfo(type="big_table", title="test_widget", size=2),
        ),
        (
            pd.DataFrame({"target": [1, 2, 3, 4], "prediction": [1, 2, 3, 4]}),
            pd.DataFrame({"target": [1, 2, 3, 1], "prediction": [1, 2, 3, 4]}),
            ColumnMapping(),
            BaseWidgetInfo(type="big_table", title="test_widget", size=2),
        ),
        (
            pd.DataFrame(
                {
                    "my_target": [1, 2, 3, 4],
                    "my_prediction": [1, 2, 3, 1],
                    "num_feature": [2, 4, 3, 5],
                    "cat_feature_1": [2, 4, 3, 5],
                    "cat_feature_2": ["a", "b", "a", "d"],
                }
            ),
            pd.DataFrame(
                {
                    "my_target": [1, 2, 1, 4],
                    "my_prediction": [1, 2, 1, 4],
                    "num_feature": [2, 2, 3, 5],
                    "cat_feature_1": [2, 4, 3, 5],
                    "cat_feature_2": ["a", "b", "b", "d"],
                }
            ),
            ColumnMapping(
                target="my_target",
                prediction="my_prediction",
                numerical_features=["num_feature"],
                categorical_features=["cat_feature_1", "cat_feature_2"],
            ),
            BaseWidgetInfo(type="big_table", title="test_widget", size=2),
        ),
        (
            pd.DataFrame(
                {
                    "my_target": [1, 2, 3, 4],
                    "my_prediction": [1, 2, 3, 1],
                    "num_feature": [2, 4, 3, 5],
                    "cat_feature_1": [2, 4, 3, 5],
                    "cat_feature_2": ["a", "b", "a", "d"],
                }
            ),
            pd.DataFrame(
                {
                    "my_target": [1, 2, 1, 4],
                    "my_prediction": [1, 2, 1, 4],
                    "num_feature": [2, 2, 3, 5],
                    "cat_feature_1": [2, 4, 3, 5],
                    "cat_feature_2": ["a", "b", "b", "d"],
                }
            ),
            ColumnMapping(
                target=None,
                prediction="my_prediction",
                numerical_features=["num_feature"],
                categorical_features=["cat_feature_1", "cat_feature_2"],
            ),
            BaseWidgetInfo(type="big_table", title="test_widget", size=2),
        ),
        (
            pd.DataFrame(
                {
                    "my_target": [1, 2, 3, 4],
                    "my_prediction": [1, 2, 3, 1],
                    "num_feature": [2, 4, 3, 5],
                    "cat_feature_1": [2, 4, 3, 5],
                    "cat_feature_2": ["a", "b", "a", "d"],
                }
            ),
            pd.DataFrame(
                {
                    "my_target": [1, 2, 1, 4],
                    "my_prediction": [1, 2, 1, 4],
                    "num_feature": [2, 2, 3, 5],
                    "cat_feature_1": [2, 4, 3, 5],
                    "cat_feature_2": ["a", "b", "b", "d"],
                }
            ),
            ColumnMapping(
                target="my_target",
                prediction=None,
                numerical_features=["num_feature"],
                categorical_features=["cat_feature_1", "cat_feature_2"],
            ),
            BaseWidgetInfo(type="big_table", title="test_widget", size=2),
        ),
    ),
)
def test_cat_target_pred_feature_table_widget(
    widget: CatTargetPredFeatureTable,
    reference_data: pd.DataFrame,
    current_data: pd.DataFrame,
    data_mapping: ColumnMapping,
    expected_result: BaseWidgetInfo,
) -> None:

    analyzer = CatTargetDriftAnalyzer()
    analyzer.options_provider = widget.options_provider
    analyzer_results = analyzer.calculate(reference_data, current_data, data_mapping)
    result = widget.calculate(
        reference_data,
        current_data,
        data_mapping,
        {CatTargetDriftAnalyzer: analyzer_results},
    )

    assert result.type == expected_result.type
    assert result.title == expected_result.title
    assert result.size == expected_result.size
    assert result.params is not None


@pytest.mark.parametrize(
    "reference_data, current_data, data_mapping",
    (
        # no target or prediction
        (
            pd.DataFrame({"data": [1, 2, 3, 4]}),
            None,
            ColumnMapping(),
        ),
        # no target or prediction
        (
            pd.DataFrame({"data": [1, 2, 3, 4]}),
            None,
            ColumnMapping(target=None, prediction=None),
        ),
    ),
)
def test_cat_target_pred_feature_table_widget_value_error(
    widget: CatTargetPredFeatureTable,
    reference_data: pd.DataFrame,
    current_data: pd.DataFrame,
    data_mapping: ColumnMapping,
) -> None:
    analyzer = CatTargetDriftAnalyzer()
    analyzer.options_provider = widget.options_provider

    # replace None current data to reference data for passing analyzers step
    if current_data is None:
        current_data_for_analyzer = reference_data

    else:
        current_data_for_analyzer = current_data

    analyzer_results = analyzer.calculate(
        reference_data, current_data_for_analyzer, data_mapping
    )

    with pytest.raises(ValueError):
        widget.calculate(
            reference_data,
            current_data,
            data_mapping,
            {CatTargetDriftAnalyzer: analyzer_results},
        )
