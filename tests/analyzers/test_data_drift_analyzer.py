import pytest
from pandas import DataFrame

from evidently import ColumnMapping
from evidently.analyzers.data_drift_analyzer import DataDriftAnalyzer
from evidently.options import DataDriftOptions, OptionsProvider


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
    analyzer.calculate(DataFrame(reference), DataFrame(current), column_mapping)


def test_data_drift_analyzer_as_dict_format(data_drift_analyzer: DataDriftAnalyzer) -> None:
    test_data = DataFrame(
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
    assert result.metrics.n_features == 5
    assert result.columns.cat_feature_names == ["categorical_feature_1", "categorical_feature_2", "target"]
    assert result.columns.num_feature_names == ["numerical_feature_1", "numerical_feature_2"]
    assert "numerical_feature_1" in result.metrics.features
    assert "numerical_feature_2" in result.metrics.features
    assert "categorical_feature_1" in result.metrics.features
    assert "categorical_feature_2" in result.metrics.features
    assert "numerical_feature_3" not in result.metrics.features

    # check data drift results
    assert result.columns.target_names == ["drift_target"]
    assert result.metrics.dataset_drift is True
