from typing import Optional

import numpy as np
import pandas as pd

import pytest
from pytest import approx

from evidently.pipeline import column_mapping
from evidently.analyzers.classification_performance_analyzer import ClassificationPerformanceAnalyzer
from evidently.analyzers.classification_performance_analyzer import ClassificationPerformanceMetrics
from evidently.analyzers.classification_performance_analyzer import ConfusionMatrix


@pytest.fixture
def analyzer() -> ClassificationPerformanceAnalyzer:
    return ClassificationPerformanceAnalyzer()


@pytest.mark.parametrize(
    "reference_data, current_data, data_mapping",
    (
        # prediction dataset only, current dataset is missed
        (
            pd.DataFrame({"target": [1, 0, 1, 1, 0, 1], "prediction": [1, 1, 0, 1, 0, 1]}),
            None,
            column_mapping.ColumnMapping(),
        ),
        # prediction dataset is missed
        (
            pd.DataFrame({"target": [1, 0, 1, 1, 0, 1], "prediction": [1, 1, 0, 1, 0, 1]}),
            pd.DataFrame({"target": [1, 0, 0, 1, 1, 1], "prediction": [0, 1, 0, 1, 0, 0]}),
            column_mapping.ColumnMapping(),
        ),
        # test with target and prediction columns mapping
        (
            pd.DataFrame({"test_target": [1, 0, 1, 1, 0, 1], "test_prediction": [1, 1, 0, 1, 0, 1]}),
            pd.DataFrame({"test_target": [1, 0, 0, 1, 1, 1], "test_prediction": [0, 1, 0, 1, 0, 0]}),
            column_mapping.ColumnMapping(target="test_target", prediction="test_prediction"),
        ),
    ),
)
def test_classification_analyser_with_numeric_binary_data(
    analyzer: ClassificationPerformanceAnalyzer,
    reference_data: pd.DataFrame,
    current_data: pd.DataFrame,
    data_mapping: Optional[column_mapping.ColumnMapping],
) -> None:
    result = analyzer.calculate(
        reference_data=reference_data,
        current_data=current_data,
        column_mapping=data_mapping,
    )
    assert result.columns is not None
    assert result.columns.target_names is None
    assert result.reference_metrics is not None
    assert result.reference_metrics.accuracy == approx(0.66666, abs=1e-5)
    assert result.reference_metrics.precision == 0.625
    assert result.reference_metrics.recall == 0.625
    assert result.reference_metrics.f1 == 0.625
    assert result.reference_metrics.metrics_matrix == {
        "0": {"f1-score": 0.5, "precision": 0.5, "recall": 0.5, "support": 2},
        "1": {"f1-score": 0.75, "precision": 0.75, "recall": 0.75, "support": 4},
        "accuracy": approx(0.66666, abs=1e-5),
        "macro avg": {
            "f1-score": 0.625,
            "precision": 0.625,
            "recall": 0.625,
            "support": 6,
        },
        "weighted avg": {
            "f1-score": approx(0.66666, abs=1e-5),
            "precision": approx(0.66666, abs=1e-5),
            "recall": approx(0.66666, abs=1e-5),
            "support": 6,
        },
    }
    # check confusion matrix values: we have only two classes - 0 and 1
    assert result.reference_metrics.confusion_matrix.labels == [0, 1]
    assert result.reference_metrics.confusion_matrix.values == [[1, 1], [1, 3]]

    if current_data is None:
        # current dataset is missed
        assert result.current_metrics is None

    else:
        # check metrics for current data
        assert result.current_metrics is not None
        assert result.current_metrics.accuracy == approx(0.33333, abs=1e-5)
        assert result.current_metrics.precision == 0.375
        assert result.current_metrics.recall == 0.375
        assert result.current_metrics.f1 == approx(0.33333, abs=1e-5)
        # skip checking of concrete metrics values for current data for metrics matrix and confusion matrix
        # we did it for reference dataset
        assert result.current_metrics.metrics_matrix is not None
        assert result.reference_metrics.confusion_matrix is not None


@pytest.mark.parametrize(
    "reference_data, data_mapping, expected_metrics",
    (
        # target and prediction are the same
        (
            pd.DataFrame({"target": ["n", "y", "n", "y"], "prediction": ["n", "y", "n", "y"]}),
            column_mapping.ColumnMapping(),
            ClassificationPerformanceMetrics(
                accuracy=1.0,
                precision=1.0,
                recall=1.0,
                f1=1.0,
                metrics_matrix={
                    "n": {"precision": 1.0, "recall": 1.0, "f1-score": 1.0, "support": 2},
                    "y": {"precision": 1.0, "recall": 1.0, "f1-score": 1.0, "support": 2},
                    "accuracy": 1.0,
                    "macro avg": {"precision": 1.0, "recall": 1.0, "f1-score": 1.0, "support": 4},
                    "weighted avg": {"precision": 1.0, "recall": 1.0, "f1-score": 1.0, "support": 4},
                },
                confusion_matrix=ConfusionMatrix(labels=["n", "y"], values=[[2, 0], [0, 2]]),
                confusion_by_classes={
                    "n": {"tp": 2, "tn": 2, "fp": 0, "fn": 0},
                    "y": {"tp": 2, "tn": 2, "fp": 0, "fn": 0},
                },
            ),
        ),
        # prediction dataset only, current dataset is missed
        (
            pd.DataFrame({"target": ["n", "n", "n", "n"], "prediction": ["y", "y", "y", "y"]}),
            column_mapping.ColumnMapping(),
            ClassificationPerformanceMetrics(
                accuracy=0.0,
                precision=0.0,
                recall=0.0,
                f1=0.0,
                metrics_matrix={
                    "n": {"precision": 0.0, "recall": 0.0, "f1-score": 0.0, "support": 4.0},
                    "y": {"precision": 0.0, "recall": 0.0, "f1-score": 0.0, "support": 0.0},
                    "accuracy": 0.0,
                    "macro avg": {"precision": 0.0, "recall": 0.0, "f1-score": 0.0, "support": 4.0},
                    "weighted avg": {"precision": 0.0, "recall": 0.0, "f1-score": 0.0, "support": 4.0},
                },
                confusion_matrix=ConfusionMatrix(labels=["n", "y"], values=[[0, 4], [0, 0]]),
                confusion_by_classes={
                    "n": {"tp": 0, "tn": 0, "fp": 0, "fn": 4},
                    "y": {"tp": 0, "tn": 0, "fp": 4, "fn": 0},
                },
            ),
        ),
        # skip infinite and NaN values in target and prediction
        (
            pd.DataFrame(
                {
                    "target": ["n", -np.inf, np.inf, "n", "y", "n", "y"],
                    "prediction": ["n", "n", "n", "y", "y", "y", np.nan],
                }
            ),
            column_mapping.ColumnMapping(),
            ClassificationPerformanceMetrics(
                accuracy=0.5,
                precision=approx(0.66666, abs=1e-5),  # noqa
                recall=approx(0.66666, abs=1e-5),  # noqa
                f1=0.5,
                metrics_matrix={
                    "n": {"precision": 1.0, "recall": approx(0.33333, abs=1e-5), "f1-score": 0.5, "support": 3},
                    "y": {"precision": approx(0.33333, abs=1e-5), "recall": 1.0, "f1-score": 0.5, "support": 1},
                    "accuracy": 0.5,
                    "macro avg": {
                        "precision": approx(0.66666, abs=1e-5),
                        "recall": approx(0.66666, abs=1e-5),
                        "f1-score": 0.5,
                        "support": 4,
                    },
                    "weighted avg": {
                        "precision": approx(0.83333, abs=1e-5),
                        "recall": 0.5,
                        "f1-score": 0.5,
                        "support": 4,
                    },
                },
                confusion_matrix=ConfusionMatrix(labels=["n", "y"], values=[[1, 2], [0, 1]]),
                confusion_by_classes={
                    "n": {"tp": 1, "tn": 1, "fp": 0, "fn": 2},
                    "y": {"tp": 1, "tn": 1, "fp": 2, "fn": 0},
                },
            ),
        ),
        # non-binary classification
        (
            pd.DataFrame({"target": ["v1", "v2", "v3", "v1"], "prediction": ["v3", "v2", "v3", "v2"]}),
            column_mapping.ColumnMapping(),
            ClassificationPerformanceMetrics(
                accuracy=0.5,
                precision=0.3333333333333333,
                recall=0.6666666666666666,
                f1=0.4444444444444444,
                metrics_matrix={
                    "v1": {"precision": 0.0, "recall": 0.0, "f1-score": 0.0, "support": 2},
                    "v2": {"precision": 0.5, "recall": 1.0, "f1-score": 0.6666666666666666, "support": 1},
                    "v3": {"precision": 0.5, "recall": 1.0, "f1-score": 0.6666666666666666, "support": 1},
                    "accuracy": 0.5,
                    "macro avg": {
                        "precision": 0.3333333333333333,
                        "recall": 0.6666666666666666,
                        "f1-score": 0.4444444444444444,
                        "support": 4,
                    },
                    "weighted avg": {"precision": 0.25, "recall": 0.5, "f1-score": 0.3333333333333333, "support": 4},
                },
                confusion_matrix=ConfusionMatrix(labels=["v1", "v2", "v3"], values=[[0, 1, 1], [0, 1, 0], [0, 0, 1]]),
                confusion_by_classes={
                    "v1": {"tp": 0, "tn": 2, "fp": 0, "fn": 2},
                    "v2": {"tp": 1, "tn": 2, "fp": 1, "fn": 0},
                    "v3": {"tp": 1, "tn": 2, "fp": 1, "fn": 0},
                },
            ),
        ),
        # non-binary classification, fewer value types in target
        (
            pd.DataFrame({"target": ["v1", "v1", "v1", "v1"], "prediction": ["v1", "v2", "v3", "v4"]}),
            column_mapping.ColumnMapping(),
            ClassificationPerformanceMetrics(
                accuracy=0.25,
                precision=0.25,
                recall=0.0625,
                f1=0.1,
                metrics_matrix={
                    "v1": {"precision": 1.0, "recall": 0.25, "f1-score": 0.4, "support": 4},
                    "v2": {"precision": 0.0, "recall": 0.0, "f1-score": 0.0, "support": 0},
                    "v3": {"precision": 0.0, "recall": 0.0, "f1-score": 0.0, "support": 0},
                    "v4": {"precision": 0.0, "recall": 0.0, "f1-score": 0.0, "support": 0},
                    "accuracy": 0.25,
                    "macro avg": {"precision": 0.25, "recall": 0.0625, "f1-score": 0.1, "support": 4},
                    "weighted avg": {"precision": 1.0, "recall": 0.25, "f1-score": 0.4, "support": 4},
                },
                confusion_matrix=ConfusionMatrix(
                    labels=["v1", "v2", "v3", "v4"], values=[[1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
                ),
                confusion_by_classes={
                    "v1": {"tp": 1, "tn": 0, "fp": 0, "fn": 3},
                    "v2": {"tp": 0, "tn": 3, "fp": 1, "fn": 0},
                    "v3": {"tp": 0, "tn": 3, "fp": 1, "fn": 0},
                    "v4": {"tp": 0, "tn": 3, "fp": 1, "fn": 0},
                },
            ),
        ),
    ),
)
def test_classification_performance_metrics_with_reference_data(
    analyzer: ClassificationPerformanceAnalyzer,
    reference_data: pd.DataFrame,
    data_mapping: Optional[column_mapping.ColumnMapping],
    expected_metrics: ClassificationPerformanceMetrics,
) -> None:
    result = analyzer.calculate(
        reference_data=reference_data,
        current_data=None,
        column_mapping=data_mapping,
    )
    assert result.columns is not None
    assert result.columns.target_names is None
    assert result.reference_metrics == expected_metrics
    assert result.current_metrics is None


@pytest.mark.parametrize(
    "reference_data, data_mapping",
    (
        # simple target names mapping
        (
            pd.DataFrame({"target": [1, 0, 1, 1, 0, 1], "prediction": [1, 1, 0, 1, 0, 1]}),
            column_mapping.ColumnMapping(target_names=["false", "true"]),
        ),
        # test with mapping for target and prediction and target names
        (
            pd.DataFrame({"another_target": [1, 0, 1, 1, 0, 1], "another_prediction": [1, 1, 0, 1, 0, 1]}),
            column_mapping.ColumnMapping(
                target="another_target", prediction="another_prediction", target_names=["false", "true"]
            ),
        ),
        # second class is in prediction column only
        (
            pd.DataFrame({"another_target": [0, 0, 0, 0, 0], "prediction": [0, 1, 0, 0, 0]}),
            column_mapping.ColumnMapping(target="another_target", target_names=["false", "true"]),
        ),
    ),
)
def test_classification_analyser_with_target_names(
    analyzer: ClassificationPerformanceAnalyzer,
    reference_data: pd.DataFrame,
    data_mapping: Optional[column_mapping.ColumnMapping],
) -> None:
    result = analyzer.calculate(
        reference_data=reference_data,
        current_data=None,
        column_mapping=data_mapping,
    )
    assert result.columns.target_names == ["false", "true"]
    # target_names now changes labels for confusion matrix only
    assert "0" in result.reference_metrics.metrics_matrix
    assert "1" in result.reference_metrics.metrics_matrix
    assert result.reference_metrics.confusion_matrix.labels == ["false", "true"]


@pytest.mark.parametrize(
    "reference_data, current_data, data_mapping",
    (
        # prediction and current datasets are missed
        (
            None,
            None,
            column_mapping.ColumnMapping(),
        ),
        # prediction dataset is missed
        (
            None,
            pd.DataFrame({"target": [0, 1, 1, 0, 1], "prediction": [1, 1, 0, 0, 1]}),
            column_mapping.ColumnMapping(),
        ),
        # data mapping is missed
        (
            pd.DataFrame({"target": [0, 1, 1, 0, 1], "prediction": [1, 1, 0, 0, 1]}),
            pd.DataFrame({"target": [0, 1, 1, 0, 1], "prediction": [1, 1, 0, 0, 1]}),
            None,
        ),
    ),
)
def test_missed_datasets_cases(
    analyzer: ClassificationPerformanceAnalyzer,
    reference_data: pd.DataFrame,
    current_data: pd.DataFrame,
    data_mapping: Optional[column_mapping.ColumnMapping],
) -> None:
    with pytest.raises(ValueError):
        analyzer.calculate(
            reference_data=reference_data,
            current_data=current_data,
            column_mapping=data_mapping,
        )


@pytest.mark.parametrize(
    "reference_data, current_data, data_mapping",
    (
        # target column is missed in data mapping
        (
            pd.DataFrame({"target": [0, 1, 1, 0, 1], "prediction": [1, 1, 0, 0, 1]}),
            pd.DataFrame({"target": [0, 1, 1, 0, 1]}),
            column_mapping.ColumnMapping(target=None),
        ),
        # prediction column is missed in data mapping
        (
            pd.DataFrame({"target": [0, 1, 1, 0, 1]}),
            None,
            column_mapping.ColumnMapping(target="another_target", prediction=None),
        ),
        # target is incorrect in data mapping
        (
            pd.DataFrame({"target": [0, 1, 1, 0, 1], "prediction": [1, 1, 0, 0, 1]}),
            pd.DataFrame({"target": [0, 1, 1, 0, 1], "prediction": [1, 1, 0, 0, 1]}),
            column_mapping.ColumnMapping(target="another_target"),
        ),
        # prediction is incorrect in data mapping
        (
            pd.DataFrame({"target": [0, 1, 1, 0, 1], "prediction": [1, 1, 0, 0, 1]}),
            pd.DataFrame({"target": [0, 1, 1, 0, 1], "prediction": [1, 1, 0, 0, 1]}),
            column_mapping.ColumnMapping(target="another_prediction"),
        ),
        # no data mapping but target and prediction columns have not default names
        (
            pd.DataFrame({"another_target": [0, 1, 1, 0, 1], "another_prediction": [1, 1, 0, 0, 1]}),
            pd.DataFrame({"another_target": [0, 1, 1, 0, 1], "another_prediction": [1, 1, 0, 0, 1]}),
            column_mapping.ColumnMapping(),
        ),
    ),
)
def test_incorrect_data_mapping_in_datasets(
    analyzer: ClassificationPerformanceAnalyzer,
    reference_data: pd.DataFrame,
    current_data: pd.DataFrame,
    data_mapping: Optional[column_mapping.ColumnMapping],
) -> None:
    result = analyzer.calculate(
        reference_data=reference_data,
        current_data=current_data,
        column_mapping=data_mapping,
    )
    assert result.reference_metrics is None
    assert result.current_metrics is None
