import pandas as pd
import pytest

from evidently import ColumnMapping
from evidently.analyzers.data_drift_analyzer import DataDriftAnalyzer
from evidently.options import DataDriftOptions
from evidently.options import OptionsProvider


@pytest.fixture
def data_drift_analyzer() -> DataDriftAnalyzer:
    options_provider: OptionsProvider = OptionsProvider()
    options_provider.add(DataDriftOptions())
    analyzer = DataDriftAnalyzer()
    analyzer.options_provider = options_provider
    return analyzer


def sample_data(feature1, feature2, feature3):
    return [{"feature1": t[0], "feature2": t[1], "feature3": t[2]} for t in zip(feature1, feature2, feature3)]


@pytest.mark.parametrize(
    ["reference", "current", "column_mapping"],
    [
        (sample_data([1], [1], [1]), sample_data([1], [1], [1]), ColumnMapping()),
        (sample_data(["1"], [1], [1]), sample_data(["1"], [1], [1]), ColumnMapping()),
        (sample_data([True], [1], [1]), sample_data([True], [1], [1]), ColumnMapping()),
    ],
)
def test_data_drift_analyzer_no_exceptions(reference, current, column_mapping):
    analyzer = DataDriftAnalyzer()
    analyzer.options_provider = OptionsProvider()
    analyzer.calculate(pd.DataFrame(reference), pd.DataFrame(current), column_mapping)


def test_data_drift_analyzer_as_dict_format(data_drift_analyzer: DataDriftAnalyzer) -> None:
    test_data = pd.DataFrame(
        {
            "target": [1, 2, 3, 4],
            "numerical_feature_1": [0.5, 0.0, 4.8, 2.1],
            "numerical_feature_2": [0, 5, 6, 3],
            "numerical_feature_3": [4, 5.5, 4, 0],
            "categorical_feature_1": [1, 1, 0, 1],
            "categorical_feature_2": [0, 1, 0, 0],
        }
    )

    data_columns = ColumnMapping()
    data_columns.numerical_features = ["numerical_feature_1", "numerical_feature_2"]
    data_columns.categorical_features = ["categorical_feature_1", "categorical_feature_2"]
    data_columns.target_names = ["drift_target"]
    result = data_drift_analyzer.calculate(test_data[:2], test_data, data_columns)
    assert result.options is not None
    assert result.columns is not None
    # check features in results
    assert result.metrics.number_of_columns == 5
    assert result.columns.cat_feature_names == ["categorical_feature_1", "categorical_feature_2"]
    assert result.columns.num_feature_names == ["numerical_feature_1", "numerical_feature_2"]
    assert "numerical_feature_1" in result.metrics.drift_by_columns
    assert "numerical_feature_2" in result.metrics.drift_by_columns
    assert "categorical_feature_1" in result.metrics.drift_by_columns
    assert "categorical_feature_2" in result.metrics.drift_by_columns
    assert "numerical_feature_3" not in result.metrics.drift_by_columns

    # check data drift results
    assert result.columns.target_names == ["drift_target"]
    assert result.metrics.dataset_drift is True


def test_data_drift_analyzer_with_different_values_in_reference_and_current_data_category_feature(
    data_drift_analyzer: DataDriftAnalyzer,
) -> None:
    ref_test_data = pd.DataFrame(
        {
            "target": [1, 2, 3, 4, 5],
            "categorical_feature_1": [1, 2, 3, 4, 5],
            "categorical_feature_2": [1, 0, 1, 0, None],
        }
    )

    curr_test_data = pd.DataFrame(
        {
            "target": [9],
            # has here a value that no in the same feature in reference
            "categorical_feature_1": [10],
            "categorical_feature_2": [1],
        }
    )

    data_columns = ColumnMapping(
        categorical_features=["categorical_feature_1", "categorical_feature_2"], target="target"
    )
    result = data_drift_analyzer.calculate(
        current_data=curr_test_data, reference_data=ref_test_data, column_mapping=data_columns
    )
    assert result.options is not None
    assert result.columns is not None
    # check features in results
    assert result.metrics.number_of_columns == 3
    assert result.metrics.dataset_drift is False


@pytest.mark.parametrize(
    ["reference", "current", "column_mapping", "expect_drift"],
    (
        (
            pd.DataFrame(
                {
                    "target": [1, 2, 3, 4, 5],
                    "categorical_feature": [1001, "test", "other", 2002, "test"],
                }
            ),
            pd.DataFrame(
                {
                    "target": [9],
                    "categorical_feature": [3003],
                }
            ),
            ColumnMapping(),
            True,
        ),
        (
            pd.DataFrame(
                {
                    "target": [1, 2, 3, 4, 5],
                    "categorical_feature": ["1001", "test", "other", "2002", "test"],
                }
            ),
            pd.DataFrame(
                {
                    "target": [9],
                    "categorical_feature": [3003],
                }
            ),
            ColumnMapping(),
            True,
        ),
        (
            pd.DataFrame(
                {
                    "target": [1, 2, 3, 4, 5],
                    "categorical_feature": [1, 2, 3, "4", None],
                }
            ),
            pd.DataFrame(
                {
                    "target": [9, 5],
                    "categorical_feature": ["4", None],
                }
            ),
            ColumnMapping(),
            False,
        ),
        (
            pd.DataFrame(
                {
                    "target": [1, 2, 3, 4, 5],
                    "categorical_feature": [1, 2, 3, 5, 5],
                }
            ),
            pd.DataFrame(
                {
                    "target": [1, 2, 3, 4, 5],
                    "categorical_feature": ["test", 123, "other", 4, 5],
                }
            ),
            ColumnMapping(categorical_features=["categorical_feature"]),
            True,
        ),
        (
            pd.DataFrame(
                {
                    "target": [1, 2, 3, 4, 5] * 1000,
                    "categorical_feature": ["test1", "test2", "test3", "test4", "test5"] * 1000,
                }
            ),
            pd.DataFrame(
                {
                    "target": [1, 2, 3, 4, 5] * 1000,
                    "categorical_feature": [1, 2, 3, 4, 5] * 1000,
                }
            ),
            ColumnMapping(),
            True,
        ),
        (
            pd.DataFrame(
                {
                    "categorical_feature": [1, 2, 3, 4, 5] * 1000,
                    "target": ["test1", "test2", "test3", 1, None] * 1000,
                }
            ),
            pd.DataFrame(
                {
                    "target": [1, 2, 3, 4, 5],
                    "categorical_feature": [1, None, 3, None, 5],
                }
            ),
            ColumnMapping(),
            True,
        ),
    ),
)
def test_data_drift_analyzer_with_mixed_str_and_int_in_cat_feature(
    data_drift_analyzer: DataDriftAnalyzer,
    reference: pd.DataFrame,
    current: pd.DataFrame,
    column_mapping: ColumnMapping,
    expect_drift: bool,
) -> None:
    result = data_drift_analyzer.calculate(
        current_data=current, reference_data=reference, column_mapping=column_mapping
    )
    assert result.metrics.dataset_drift is expect_drift
