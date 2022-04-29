import numpy as np
import pandas as pd

from evidently.analyzers.utils import DatasetColumns
from evidently.analyzers.utils import DatasetUtilityColumns
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.analyzers.regression_performance_analyzer import RegressionPerformanceAnalyzer
from evidently.analyzers.regression_performance_analyzer import RegressionPerformanceMetrics
from evidently.analyzers.regression_performance_analyzer import RegressionPerformanceAnalyzerResults

import pytest
from pytest import approx


@pytest.fixture
def analyzer() -> RegressionPerformanceAnalyzer:
    return RegressionPerformanceAnalyzer()


@pytest.mark.parametrize(
    "reference_data, current_data, data_mapping, expected_result",
    (
        # reference dataset only, current dataset is missed
        (
            pd.DataFrame({"target": [1, 0, 1, 1], "prediction": [1, 1, 0, 1]}),
            None,
            ColumnMapping(),
            RegressionPerformanceAnalyzerResults(
                columns=DatasetColumns(
                    utility_columns=DatasetUtilityColumns(
                        date=None, id_column=None, target="target", prediction="prediction"
                    ),
                    num_feature_names=[],
                    cat_feature_names=[],
                    datetime_feature_names=[],
                    target_names=None,
                ),
                reference_metrics=RegressionPerformanceMetrics(
                    mean_error=0.0,
                    mean_abs_error=0.5,
                    mean_abs_perc_error=np.inf,
                    error_std=0.816496580927726,
                    abs_error_std=0.5773502691896257,
                    abs_perc_error_std=approx(np.nan, nan_ok=True),  # noqa
                    error_normality={
                        "order_statistic_medians_x": [
                            -0.9981488825015566,
                            -0.29119141829755274,
                            0.2911914182975529,
                            0.9981488825015566,
                        ],
                        "order_statistic_medians_y": [-1.0, 0.0, 0.0, 1.0],
                        "slope": 0.923276995960497,
                        "intercept": -5.125216895110457e-17,
                        "r": 0.9599832820197256,
                    },
                    underperformance={
                        "majority": {"mean_error": 0.0, "std_error": 0.0},
                        "underestimation": {"mean_error": -1.0, "std_error": approx(np.nan, nan_ok=True)},
                        "overestimation": {"mean_error": 1.0, "std_error": approx(np.nan, nan_ok=True)},
                    },
                ),
                current_metrics=None,
                error_bias={},
            ),
        ),
        # reference and current datasets are presented
        (
            pd.DataFrame({"target": [1, 2, 3, 4], "prediction": [1, 2, 3, 4]}),
            pd.DataFrame({"target": [1, 2], "prediction": [1, 2]}),
            ColumnMapping(),
            RegressionPerformanceAnalyzerResults(
                columns=DatasetColumns(
                    utility_columns=DatasetUtilityColumns(
                        date=None, id_column=None, target="target", prediction="prediction"
                    ),
                    num_feature_names=[],
                    cat_feature_names=[],
                    datetime_feature_names=[],
                    target_names=None,
                ),
                reference_metrics=RegressionPerformanceMetrics(
                    mean_error=0.0,
                    mean_abs_error=0.0,
                    mean_abs_perc_error=0.0,
                    error_std=0.0,
                    abs_error_std=0.0,
                    abs_perc_error_std=0.0,
                    error_normality={
                        "order_statistic_medians_x": [
                            -0.9981488825015566,
                            -0.29119141829755274,
                            0.2911914182975529,
                            0.9981488825015566,
                        ],
                        "order_statistic_medians_y": [0.0, 0.0, 0.0, 0.0],
                        "slope": 0.0,
                        "intercept": 0.0,
                        "r": 0.0,
                    },
                    underperformance={
                        "majority": {
                            "mean_error": approx(np.nan, nan_ok=True),
                            "std_error": approx(np.nan, nan_ok=True),
                        },
                        "underestimation": {"mean_error": 0.0, "std_error": 0.0},
                        "overestimation": {"mean_error": 0.0, "std_error": 0.0},
                    },
                ),
                current_metrics=RegressionPerformanceMetrics(
                    mean_error=0.0,
                    mean_abs_error=0.0,
                    mean_abs_perc_error=0.0,
                    error_std=0.0,
                    abs_error_std=0.0,
                    abs_perc_error_std=0.0,
                    error_normality={
                        "order_statistic_medians_x": [-0.5449521356173604, 0.5449521356173604],
                        "order_statistic_medians_y": [0.0, 0.0],
                        "slope": 0.0,
                        "intercept": 0.0,
                        "r": 0.0,
                    },
                    underperformance={
                        "majority": {
                            "mean_error": approx(np.nan, nan_ok=True),
                            "std_error": approx(np.nan, nan_ok=True),
                        },
                        "underestimation": {"mean_error": 0.0, "std_error": 0.0},
                        "overestimation": {"mean_error": 0.0, "std_error": 0.0},
                    },
                ),
                error_bias={},
            ),
        ),
        # target and prediction columns mapping and numeric and category features
        (
            pd.DataFrame(
                {
                    "test_target": [1, 0, 1, 1],
                    "test_prediction": [1, 1, 0, 0],
                    "numeric_feature_1": [10, 10, 10, 10],
                    "numeric_feature_2": [2, 2, 3, 10],
                    "category_feature_1": [1, 1, 1, 1],
                    "category_feature_2": [1, 2, 3, 4],
                }
            ),
            pd.DataFrame(
                {
                    "test_target": [1, 0],
                    "test_prediction": [0, 1],
                    "numeric_feature_1": [10, 10],
                    "numeric_feature_2": [2, 4],
                    "category_feature_1": [1, 1],
                    "category_feature_2": [1, 2],
                }
            ),
            ColumnMapping(
                target="test_target",
                prediction="test_prediction",
                numerical_features=["numeric_feature_1", "numeric_feature_2"],
                categorical_features=["category_feature_1", "category_feature_2"],
            ),
            RegressionPerformanceAnalyzerResults(
                columns=DatasetColumns(
                    utility_columns=DatasetUtilityColumns(
                        date=None, id_column=None, target="test_target", prediction="test_prediction"
                    ),
                    num_feature_names=["numeric_feature_1", "numeric_feature_2"],
                    cat_feature_names=["category_feature_1", "category_feature_2"],
                    datetime_feature_names=[],
                    target_names=None,
                ),
                reference_metrics=RegressionPerformanceMetrics(
                    mean_error=-0.25,
                    mean_abs_error=0.75,
                    mean_abs_perc_error=np.inf,
                    error_std=0.9574271077563381,
                    abs_error_std=0.5,
                    abs_perc_error_std=approx(np.nan, nan_ok=True),  # noqa
                    error_normality={
                        "order_statistic_medians_x": [
                            -0.9981488825015566,
                            -0.29119141829755274,
                            0.2911914182975529,
                            0.9981488825015566,
                        ],
                        "order_statistic_medians_y": [-1.0, -1.0, 0.0, 1.0],
                        "slope": 1.0579514631910014,
                        "intercept": -0.25000000000000006,
                        "r": 0.9380933329232763,
                    },
                    underperformance={
                        "majority": {"mean_error": 0.0, "std_error": approx(np.nan, nan_ok=True)},
                        "underestimation": {"mean_error": -1.0, "std_error": 0.0},
                        "overestimation": {"mean_error": 1.0, "std_error": approx(np.nan, nan_ok=True)},
                    },
                ),
                current_metrics=RegressionPerformanceMetrics(
                    mean_error=0.0,
                    mean_abs_error=1.0,
                    mean_abs_perc_error=np.inf,
                    error_std=1.4142135623730951,
                    abs_error_std=0.0,
                    abs_perc_error_std=approx(np.nan, nan_ok=True),  # noqa
                    error_normality={
                        "order_statistic_medians_x": [-0.5449521356173604, 0.5449521356173604],
                        "order_statistic_medians_y": [-1.0, 1.0],
                        "slope": 1.8350235454479484,
                        "intercept": 0.0,
                        "r": 1.0,
                    },
                    underperformance={
                        "majority": {
                            "mean_error": approx(np.nan, nan_ok=True),
                            "std_error": approx(np.nan, nan_ok=True),
                        },
                        "underestimation": {"mean_error": -1.0, "std_error": approx(np.nan, nan_ok=True)},
                        "overestimation": {"mean_error": 1.0, "std_error": approx(np.nan, nan_ok=True)},
                    },
                ),
                error_bias={
                    "numeric_feature_1": {
                        "feature_type": "num",
                        "ref_majority": 10.0,
                        "ref_under": 10.0,
                        "ref_over": 10.0,
                        "ref_range": 0.0,
                        "current_majority": 10.0,
                        "current_under": 10.0,
                        "current_over": 10.0,
                        "current_range": 0.0,
                    },
                    "numeric_feature_2": {
                        "feature_type": "num",
                        "ref_majority": 4.25,
                        "ref_under": 6.5,
                        "ref_over": 2.0,
                        "ref_range": 56.25,
                        "current_majority": 3.0,
                        "current_under": 2.0,
                        "current_over": 4.0,
                        "current_range": 100.0,
                    },
                    "category_feature_1": {
                        "feature_type": "cat",
                        "ref_majority": 1.0,
                        "ref_under": 1.0,
                        "ref_over": 1.0,
                        "ref_range": 0.0,
                        "current_majority": 1.0,
                        "current_under": 1.0,
                        "current_over": 1.0,
                        "current_range": 0.0,
                    },
                    "category_feature_2": {
                        "feature_type": "cat",
                        "ref_majority": 4.0,
                        "ref_under": 3.0,
                        "ref_over": 2.0,
                        "ref_range": 1.0,
                        "current_majority": 2.0,
                        "current_under": 1.0,
                        "current_over": 2.0,
                        "current_range": 1.0,
                    },
                },
            ),
        ),
    ),
)
def test_regression_performance_analyser(
    analyzer: RegressionPerformanceAnalyzer,
    reference_data: pd.DataFrame,
    current_data: pd.DataFrame,
    data_mapping: ColumnMapping,
    expected_result: RegressionPerformanceAnalyzerResults,
) -> None:
    result = analyzer.calculate(
        reference_data=reference_data,
        current_data=current_data,
        column_mapping=data_mapping,
    )
    assert result == expected_result
