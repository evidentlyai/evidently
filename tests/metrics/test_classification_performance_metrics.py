from typing import Optional
from typing import Tuple
from typing import Union

import numpy as np
import pandas as pd
import pytest
from pytest import approx

from evidently.calculations.classification_performance import ConfusionMatrix
from evidently.calculations.classification_performance import get_prediction_data
from evidently.calculations.classification_performance import k_probability_threshold
from evidently.calculations.classification_performance import threshold_probability_labels
from evidently.metrics import ClassificationPerformanceMetrics
from evidently.metrics import ClassificationPerformanceMetricsThreshold
from evidently.metrics import ClassificationPerformanceMetricsTopK
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.report import Report
from evidently.utils.data_operations import process_columns


def test_classification_performance_metrics_binary_labels() -> None:
    test_dataset = pd.DataFrame(
        {
            "target": [1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            "prediction": [1, 1, 0, 1, 0, 0, 1, 0, 0, 1],
        }
    )
    column_mapping = ColumnMapping(target="target", prediction="prediction")
    metric = ClassificationPerformanceMetrics()
    report = Report(metrics=[metric])
    report.run(current_data=test_dataset, reference_data=None, column_mapping=column_mapping)
    result = metric.get_result()
    assert result is not None
    assert result.current.accuracy == 0.7
    assert result.current.precision == 0.6
    assert result.current.recall == 0.75
    assert result.current.f1 == 0.6666666666666665
    assert result.current.metrics_matrix == {
        "0": {"precision": 0.8, "recall": 0.6666666666666666, "f1-score": 0.7272727272727272, "support": 6},
        "1": {"precision": 0.6, "recall": 0.75, "f1-score": 0.6666666666666665, "support": 4},
        "accuracy": 0.7,
        "macro avg": {"precision": 0.7, "recall": 0.7083333333333333, "f1-score": 0.6969696969696968, "support": 10},
        "weighted avg": {"precision": 0.7200000000000001, "recall": 0.7, "f1-score": 0.7030303030303029, "support": 10},
    }
    assert result.current.confusion_matrix == ConfusionMatrix(labels=["0", "1"], values=[[4, 2], [1, 3]])


def test_classification_performance_metrics_with_report() -> None:
    test_dataset = pd.DataFrame(
        {
            "my_target": [1, 1, 0],
            "my_prediction": [0, 1, 1],
        }
    )
    data_mapping = ColumnMapping(target="my_target", prediction="my_prediction")
    report = Report(metrics=[ClassificationPerformanceMetrics()])
    report.run(current_data=test_dataset, reference_data=None, column_mapping=data_mapping)
    assert report.show()
    assert report.json()

    report.run(current_data=test_dataset, reference_data=test_dataset, column_mapping=data_mapping)
    assert report.show()
    assert report.json()


def test_classification_performance_metrics_probs_with_report() -> None:
    test_dataset = pd.DataFrame(
        {
            "label_a": [0.5, 0.4, 0.1],
            "label_b": [0.5, 0.4, 0.1],
            "label_c": [0.9, 0.2, 0.3],
            "target": ["label_a", "label_b", "label_c"],
        }
    )
    data_mapping = ColumnMapping(prediction=["label_a", "label_b", "label_c"])
    report = Report(metrics=[ClassificationPerformanceMetrics()])
    report.run(current_data=test_dataset, reference_data=test_dataset, column_mapping=data_mapping)
    assert report.show()
    assert report.json()


def test_classification_performance_metrics_binary_probas_threshold() -> None:
    test_dataset = pd.DataFrame(
        {
            "target": [1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            "prediction": [0.9, 0.7, 0.0, 0.5, 0.1, 0.4, 0.6, 0.2, 0.2, 0.8],
        }
    )
    class_threshold = 0.6
    column_mapping = ColumnMapping(target="target", prediction="prediction")
    metric = ClassificationPerformanceMetricsThreshold(class_threshold)
    report = Report(metrics=[metric])
    report.run(current_data=test_dataset, reference_data=None, column_mapping=column_mapping)
    result = metric.get_result()
    assert result is not None
    assert result.current.accuracy == 0.6
    assert result.current.precision == 0.5
    assert result.current.recall == 0.5
    assert result.current.f1 == 0.5
    assert result.current.roc_auc == 0.625
    assert result.current.log_loss == 3.928216092142768
    assert result.current.confusion_matrix == ConfusionMatrix(labels=["0", "1"], values=[[4, 2], [2, 2]])


def test_classification_performance_metrics_binary_probas_threshold_with_report() -> None:
    test_dataset = pd.DataFrame(
        {
            "target": [1, 1, 0],
            "prediction": [0.9, 0.7, 0.0],
        }
    )
    data_mapping = ColumnMapping(target="target", prediction="prediction")
    report = Report(metrics=[ClassificationPerformanceMetricsThreshold(threshold=1)])
    report.run(current_data=test_dataset, reference_data=None, column_mapping=data_mapping)
    assert report.show()
    assert report.json()

    report.run(current_data=test_dataset, reference_data=test_dataset, column_mapping=data_mapping)
    assert report.show()
    assert report.json()


@pytest.mark.parametrize(
    "data,mapping,expected_predictions,expected_probas",
    [
        # just simple target and predictions, without probabilities
        # return predictions and no probas
        (
            pd.DataFrame({"target": [1, 0, 1], "predictions": [0, 0, 1]}),
            ColumnMapping(prediction="predictions"),
            [0, 0, 1],
            None,
        ),
        # just simple target and predictions, without probabilities, no negative value
        (
            pd.DataFrame({"target": [1, 1, 1], "predictions": [1, 1, 1]}),
            ColumnMapping(prediction="predictions"),
            [1, 1, 1],
            None,
        ),
        # just simple target and predictions, without probabilities, in target only one value
        (
            pd.DataFrame({"target": [1, 1, 1], "predictions": [0, 0, 1]}),
            ColumnMapping(prediction="predictions"),
            [0, 0, 1],
            None,
        ),
        # just simple target and predictions, without probabilities, only one not-default value
        (
            pd.DataFrame({"target": ["a", "a", "a"], "predictions": ["a", "a", "a"]}),
            ColumnMapping(prediction="predictions"),
            ["a", "a", "a"],
            None,
        ),
        # multy classification, prediction is labels-strings
        (
            pd.DataFrame({"target": ["a", "a", "a"], "a": [0.1, 0.3, 0.9], "b": [0.8, 0.7, 0.1], "c": [0.9, 0.7, 0.1]}),
            ColumnMapping(prediction=["a", "b", "c"]),
            ["c", "b", "a"],
            {"a": {0: 0.1, 1: 0.3, 2: 0.9}, "b": {0: 0.8, 1: 0.7, 2: 0.1}, "c": {0: 0.9, 1: 0.7, 2: 0.1}},
        ),
        # multy classification, prediction is labels-strings, all probabilities are lower than default threshold
        (
            pd.DataFrame({"target": ["a", "a", "a"], "a": [0.1, 0.2, 0.2], "b": [0.2, 0.3, 0.1], "c": [0.3, 0.2, 0.1]}),
            ColumnMapping(prediction=["a", "b", "c"]),
            ["c", "b", "a"],
            {"a": {0: 0.1, 1: 0.2, 2: 0.2}, "b": {0: 0.2, 1: 0.3, 2: 0.1}, "c": {0: 0.3, 1: 0.2, 2: 0.1}},
        ),
        # binary classification, prediction is labels-numbers
        (
            pd.DataFrame({"target": [1, 0, 1], 1: [0.1, 0.3, 0.9], 0: [0.9, 0.7, 0.1]}),
            ColumnMapping(prediction=[1, 0]),
            [0, 0, 1],
            {0: {0: 0.9, 1: 0.7, 2: 0.1}, 1: {0: 0.1, 1: 0.3, 2: 0.9}},
        ),
        # binary classification, prediction is negative, pos label is 0
        (
            pd.DataFrame({"target": [1, 0, 1], "1": [0.1, 0.3, 0.9], 0: [0.9, 0.7, 0.1]}),
            ColumnMapping(prediction="1", pos_label=0),
            [0, 0, 1],
            {
                0: {0: 0.9, 1: 0.7, 2: approx(0.1, abs=0.01)},
                1: {0: approx(0.1, abs=0.01), 1: approx(0.3, abs=0.01), 2: 0.9},
            },
        ),
        # binary classification, prediction is labels-strings
        (
            pd.DataFrame({"target": ["true", "false", "true"], "true": [0.1, 0.3, 0.9], "false": [0.9, 0.7, 0.1]}),
            ColumnMapping(prediction=["true", "false"], pos_label="true"),
            ["false", "false", "true"],
            {"false": {0: 0.9, 1: 0.7, 2: 0.1}, "true": {0: 0.1, 1: 0.3, 2: 0.9}},
        ),
        # prediction is a one column with probabilities
        (
            pd.DataFrame({"target": ["true", "false", "true"], "true": [0.1, 0.3, 0.8]}),
            ColumnMapping(prediction="true", pos_label="true"),
            ["false", "false", "true"],
            {"false": {0: 0.9, 1: 0.7, 2: approx(0.2, abs=0.01)}, "true": {0: 0.1, 1: 0.3, 2: 0.8}},
        ),
        (
            pd.DataFrame({"target": ["a", "b"], "a": [0.9, 0.4]}),
            ColumnMapping(prediction="a", pos_label="a"),
            ["a", "b"],
            {"a": {0: 0.9, 1: 0.4}, "b": {0: approx(0.1, abs=0.01), 1: 0.6}},
        ),
        (
            pd.DataFrame({"target": ["a", "b"], "b": [0.1, 0.6]}),
            ColumnMapping(prediction="b", pos_label="a"),
            ["a", "b"],
            {"a": {0: 0.9, 1: 0.4}, "b": {0: approx(0.1, abs=0.01), 1: 0.6}},
        ),
        (
            pd.DataFrame({"target": ["a", "a"], "a": [0.9, 0.4]}),
            ColumnMapping(prediction="a", pos_label="a", target_names=["b", "a"]),
            ["a", "b"],
            {"a": {0: 0.9, 1: 0.4}, "b": {0: approx(0.1, abs=0.01), 1: 0.6}},
        ),
    ],
)
def test_prediction_data_with_default_threshold(
    data: pd.DataFrame, mapping: ColumnMapping, expected_predictions: list, expected_probas: Optional[dict]
):
    columns = process_columns(data, mapping)
    prediction_data = get_prediction_data(data, columns, mapping.pos_label)
    assert prediction_data.predictions.tolist() == expected_predictions

    if expected_probas is None:
        assert prediction_data.prediction_probas is None

    else:
        assert prediction_data.prediction_probas.to_dict() == expected_probas


@pytest.mark.parametrize(
    "data,mapping,error_text",
    [
        # no pos value
        (
            pd.DataFrame({"target": ["true", "false", "true"], "true": [0.1, 0.3, 0.8]}),
            ColumnMapping(prediction="true"),
            "Cannot find pos_label '1' in labels ['true' 'false']",
        ),
        # incorrect pos value
        (
            pd.DataFrame({"target": ["true", "false", "true"], "true": [0.1, 0.3, 0.8]}),
            ColumnMapping(prediction="true", pos_label="pos"),
            "Cannot find pos_label 'pos' in labels ['true' 'false']",
        ),
        (
            pd.DataFrame({"target": ["true", "false", "true"], "true": [0.1, 0.3, 0.8], "false": [0.9, 0.7, 0.2]}),
            ColumnMapping(prediction=["true", "false"], pos_label="pos"),
            "Cannot find pos_label 'pos' in labels ['true' 'false']",
        ),
        # prediction not in labels list
        (
            pd.DataFrame({"target": ["true", "false", "true"], "True": [0.1, 0.3, 0.8]}),
            ColumnMapping(prediction="True", pos_label="true"),
            "No prediction for the target labels were found. "
            "Consider to rename columns with the prediction to match target labels.",
        ),
    ],
)
def test_prediction_data_raises_value_error(data: pd.DataFrame, mapping: ColumnMapping, error_text: str):
    columns = process_columns(data, mapping)

    with pytest.raises(ValueError) as error:
        get_prediction_data(data, columns, pos_label=mapping.pos_label)

    assert error.value.args[0] == error_text


def test_classification_performance_metrics() -> None:
    test_dataset = pd.DataFrame({"target": [1, 1, 1, 1], "prediction": [1, 1, 1, 0]})
    data_mapping = ColumnMapping()
    metric = ClassificationPerformanceMetrics()
    report = Report(metrics=[metric])
    report.run(current_data=test_dataset, reference_data=None, column_mapping=data_mapping)
    result = metric.get_result()
    assert result is not None
    assert result.current.accuracy == 0.75
    assert result.current.f1 == approx(0.86, abs=0.01)
    assert result.current.precision == 1
    assert result.current.recall == 0.75


@pytest.mark.parametrize(
    "data, mapping, threshold, expected",
    (
        (
            pd.DataFrame(
                {
                    "target": ["a", "a", "a", "b", "b", "b", "c", "c", "c", "c"],
                    "a": [0.9, 0.8, 0.6, 0.4, 0.4, 0.3, 0.6, 0.2, 0.2, 0.1],
                    "b": [0.0, 0.1, 0.1, 0.3, 0.5, 0.1, 0.1, 0.1, 0.0, 0.2],
                    "c": [0.1, 0.1, 0.3, 0.3, 0.1, 0.6, 0.3, 0.7, 0.8, 0.7],
                }
            ),
            ColumnMapping(prediction=["a", "b", "c"], target="target"),
            0.5,
            (
                pd.Series(["a", "a", "a", "a", "b", "c", "a", "c", "c", "c"]),
                pd.DataFrame(
                    {
                        "a": [0.9, 0.8, 0.6, 0.4, 0.4, 0.3, 0.6, 0.2, 0.2, 0.1],
                        "b": [0.0, 0.1, 0.1, 0.3, 0.5, 0.1, 0.1, 0.1, 0.0, 0.2],
                        "c": [0.1, 0.1, 0.3, 0.3, 0.1, 0.6, 0.3, 0.7, 0.8, 0.7],
                    }
                ),
            ),
        ),
        (
            pd.DataFrame(
                {
                    "target": ["a", "a", "a", "a", "b", "b", "b", "b", "b", "b"],
                    "a": [0.9, 0.7, 0.0, 0.5, 0.1, 0.4, 0.6, 0.2, 0.2, 0.8],
                    "b": [0.1, 0.3, 1.0, 0.5, 0.9, 0.6, 0.4, 0.8, 0.8, 0.2],
                }
            ),
            ColumnMapping(prediction=["a", "b"], target="target", pos_label="b"),
            0.5,
            (
                pd.Series(["a", "a", "b", "b", "b", "b", "a", "b", "b", "a"]),
                pd.DataFrame(
                    {
                        "b": [0.1, 0.3, 1.0, 0.5, 0.9, 0.6, 0.4, 0.8, 0.8, 0.2],
                        "a": [0.9, 0.7, 0.0, 0.5, 0.1, 0.4, 0.6, 0.2, 0.2, 0.8],
                    }
                ),
            ),
        ),
        (
            pd.DataFrame(
                {
                    "target": ["a", "a", "a", "a", "b", "b", "b", "b", "b", "b"],
                    "b": [0.1, 0.3, 1.0, 0.5, 0.9, 0.6, 0.4, 0.8, 0.8, 0.2],
                }
            ),
            ColumnMapping(prediction="b", target="target", pos_label="b"),
            0.5,
            (
                pd.Series(["a", "a", "b", "b", "b", "b", "a", "b", "b", "a"]),
                pd.DataFrame(
                    {
                        "b": [0.1, 0.3, 1.0, 0.5, 0.9, 0.6, 0.4, 0.8, 0.8, 0.2],
                        "a": [0.9, 0.7, 0.0, 0.5, 0.1, 0.4, 0.6, 0.2, 0.2, 0.8],
                    }
                ),
            ),
        ),
        (
            pd.DataFrame(
                {"target": [1, 1, 1, 1, 0, 0, 0, 0, 0, 0], "0": [0.1, 0.3, 1.0, 0.5, 0.9, 0.6, 0.4, 0.8, 0.8, 0.2]}
            ),
            ColumnMapping(prediction="0", target="target", pos_label=0),
            0.5,
            (
                pd.Series([1, 1, 0, 0, 0, 0, 1, 0, 0, 1]),
                pd.DataFrame(
                    {
                        0: [0.1, 0.3, 1.0, 0.5, 0.9, 0.6, 0.4, 0.8, 0.8, 0.2],
                        1: [0.9, 0.7, 0.0, 0.5, 0.1, 0.4, 0.6, 0.2, 0.2, 0.8],
                    }
                ),
            ),
        ),
        (
            pd.DataFrame(
                {"target": [1, 1, 1, 1, 0, 0, 0, 0, 0, 0], "preds": [0.1, 0.3, 1.0, 0.5, 0.9, 0.6, 0.4, 0.8, 0.8, 0.2]}
            ),
            ColumnMapping(prediction="preds", target="target"),
            0.5,
            (
                pd.Series([0, 0, 1, 1, 1, 1, 0, 1, 1, 0]),
                pd.DataFrame(
                    {
                        1: [0.1, 0.3, 1.0, 0.5, 0.9, 0.6, 0.4, 0.8, 0.8, 0.2],
                        0: [0.9, 0.7, 0.0, 0.5, 0.1, 0.4, 0.6, 0.2, 0.2, 0.8],
                    }
                ),
            ),
        ),
    ),
)
def test_get_prediction_data(
    data: pd.DataFrame, mapping: ColumnMapping, threshold: float, expected: Tuple[pd.Series, Optional[pd.DataFrame]]
):
    columns = process_columns(data, mapping)
    result = get_prediction_data(data, columns, pos_label=mapping.pos_label, threshold=threshold)
    assert result.predictions.equals(expected[0])
    assert np.allclose(result.prediction_probas, expected[1])
    assert list(result.prediction_probas.columns) == list(expected[1].columns)


@pytest.mark.parametrize(
    "probas,k,expected",
    (
        (
            pd.DataFrame(
                dict(
                    a=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.0],
                    b=[0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 1],
                )
            ),
            0.1,
            0.9,
        ),
        (
            pd.DataFrame(
                np.array(
                    [
                        [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.0],
                        [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 1],
                    ]
                ).T
            ),
            0.1,
            0.9,
        ),
        (
            pd.DataFrame(
                dict(
                    a=[0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 1],
                    b=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.0],
                )
            ),
            0.1,
            1.0,
        ),
        (
            pd.DataFrame(
                dict(
                    a=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.0],
                    b=[0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 1],
                )
            ),
            0.2,
            0.8,
        ),
        (
            pd.DataFrame(
                dict(
                    a=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.0],
                    b=[0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 1],
                )
            ),
            1,
            0.8,
        ),
        (
            pd.DataFrame(
                dict(
                    a=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.0],
                    b=[0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 1],
                )
            ),
            2,
            0.7,
        ),
        (
            pd.DataFrame(
                dict(
                    a=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.0],
                    b=[0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 1],
                )
            ),
            11,
            0.0,
        ),
        (
            pd.DataFrame(
                dict(
                    a=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.0],
                    b=[0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 1],
                )
            ),
            0.0,
            0.9,
        ),
    ),
)
def test_k_probability_threshold(probas: pd.DataFrame, k: Union[int, float], expected: float):
    assert k_probability_threshold(probas, k) == expected


@pytest.mark.parametrize(
    "probas, pos_label, neg_label, threshold, expected",
    (
        (
            pd.DataFrame(
                {
                    "a": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.0],
                    "b": [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.09, 1],
                }
            ),
            "b",
            "a",
            0.1,
            ["b", "b", "b", "b", "b", "b", "b", "b", "a", "b"],
        ),
        (
            pd.DataFrame(
                {
                    "a": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.0],
                    "b": [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 1],
                }
            ),
            "a",
            "b",
            0.84,
            ["b", "b", "b", "b", "b", "b", "b", "b", "a", "b"],
        ),
        (
            pd.DataFrame({"a": [0.1, 0.2, 0.9, 0.8, 0.9, 0.5, 0.3, 0.99, 0.1, 1]}),
            "a",
            "b",
            0.84,
            ["b", "b", "a", "b", "a", "b", "b", "a", "b", "a"],
        ),
        (
            pd.DataFrame(
                {
                    "a": [0.1, 0.2, 0.9, 0.8, 0.9, 0.5, 0.3, 0.99, 0.1, 1],
                    "b": [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 1],
                }
            ),
            "b",
            "a",
            0.84,
            ["b", "a", "a", "a", "a", "a", "a", "a", "a", "b"],
        ),
    ),
)
def test_threshold_probability_labels(
    probas: pd.DataFrame, pos_label: str, neg_label: str, threshold: float, expected: pd.Series
) -> None:
    assert threshold_probability_labels(probas, pos_label, neg_label, threshold).tolist() == expected


def test_classification_performance_top_k_metrics() -> None:
    test_dataset = pd.DataFrame(
        {
            "target": ["1", "2", "1"],
            "1": [1.0, 0.0, 0.5],
        }
    )
    data_mapping = ColumnMapping(target="target", prediction="1", pos_label="2")
    report = Report(metrics=[ClassificationPerformanceMetricsTopK(k=1)])
    report.run(current_data=test_dataset, reference_data=None, column_mapping=data_mapping)
    assert report.show()
    assert report.json()

    report.run(current_data=test_dataset, reference_data=test_dataset, column_mapping=data_mapping)
    assert report.show()
    assert report.json()


def test_classification_performance_top_k_metrics_no_probas() -> None:
    test_dataset = pd.DataFrame(
        {
            "target": [1, 1, 1],
            "prediction": [1, 1, 0],
        }
    )
    data_mapping = ColumnMapping(target="target", prediction="prediction", pos_label=1)
    report = Report(metrics=[ClassificationPerformanceMetricsTopK(k=1)])

    with pytest.raises(ValueError):
        report.run(current_data=test_dataset, reference_data=None, column_mapping=data_mapping)
        report.json()
