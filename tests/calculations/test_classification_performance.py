import numpy as np
import pandas as pd
import pytest
from sklearn import metrics

from evidently.legacy.calculations.classification_performance import calculate_confusion_by_classes
from evidently.legacy.calculations.classification_performance import calculate_metrics
from evidently.legacy.calculations.classification_performance import get_prediction_data
from evidently.legacy.metric_results import ConfusionMatrix
from evidently.legacy.metric_results import DatasetColumns
from evidently.legacy.metric_results import DatasetUtilityColumns
from evidently.legacy.metric_results import PredictionData
from evidently.legacy.pipeline.column_mapping import ColumnMapping


def test_calculate_confusion_by_classes():
    confusion_matrix = np.array([[4, 1], [2, 5]])
    labels = ["a", "b"]
    confusion_by_classes = calculate_confusion_by_classes(confusion_matrix, labels)
    assert confusion_by_classes[labels[0]] == {"tp": 4, "fn": 1, "fp": 2, "tn": 5}
    assert confusion_by_classes[labels[1]] == {"tp": 5, "fn": 2, "fp": 1, "tn": 4}


def test_calculate_metrics():
    prediction_probas = np.array([0.91, 0.82, 0.73, 0.64, 0.55, 0.46, 0.37, 0.28, 0.19, 0.0])
    target_values = [1, 0, 0, 1, 1, 1, 0, 1, 0, 0]
    thr = 0.7
    predictions = (prediction_probas >= thr).astype(int)
    labels = ["n", "y"]
    labels_map = dict(zip([0, 1], labels))
    pos_label = labels[1]

    column_mapping = ColumnMapping(pos_label=pos_label)
    confusion_matrix = ConfusionMatrix(
        labels=labels,
        values=metrics.confusion_matrix(target_values, predictions).tolist(),
    )
    target = pd.Series(target_values).map(labels_map)
    prediction = PredictionData(
        predictions=pd.Series(predictions).map(labels_map),
        labels=labels,
        prediction_probas=pd.DataFrame({labels[0]: 1 - prediction_probas, labels[1]: prediction_probas}),
    )

    actual_result = calculate_metrics(column_mapping, confusion_matrix, target, prediction)

    assert actual_result.accuracy == pytest.approx(4 / 10)
    assert actual_result.precision == pytest.approx(1 / 3)
    assert actual_result.recall == pytest.approx(1 / 5)
    assert actual_result.f1 == pytest.approx(1 / 4)
    assert actual_result.tpr == pytest.approx(1 / 5)
    assert actual_result.tnr == pytest.approx(3 / 5)
    assert actual_result.fpr == pytest.approx(2 / 5)
    assert actual_result.fnr == pytest.approx(4 / 5)
    assert actual_result.roc_auc == pytest.approx(0.64)
    assert actual_result.log_loss == pytest.approx(0.6884817487155065)

    # In `thrs` the 1st elem can be 1.91 or inf depending on version
    assert actual_result.rate_plots_data.thrs[1:] == [pytest.approx(v) for v in [0.91, 0.73, 0.46, 0.37, 0.28, 0.0]]
    assert actual_result.rate_plots_data.tpr == [pytest.approx(v) for v in [0.0, 0.2, 0.2, 0.8, 0.8, 1.0, 1.0]]
    assert actual_result.rate_plots_data.fpr == [pytest.approx(v) for v in [0.0, 0.0, 0.4, 0.4, 0.6, 0.6, 1.0]]
    assert actual_result.rate_plots_data.fnr == [pytest.approx(v) for v in [1.0, 0.8, 0.8, 0.2, 0.2, 0.0, 0.0]]
    assert actual_result.rate_plots_data.tnr == [pytest.approx(v) for v in [1.0, 1.0, 0.6, 0.6, 0.4, 0.4, 0.0]]


@pytest.mark.parametrize(
    "dataframe,target,prediction,target_names,pos_label,expected",
    (
        (
            pd.DataFrame(data={"col": ["a", "b", "b", "a", "b"], "prob": [0.1, 0.1, 0.1, 0.8, 0.2]}),
            "col",
            "prob",
            ["a", "b"],
            "a",
            {"a": [0.1, 0.1, 0.1, 0.8, 0.2], "b": [0.9, 0.9, 0.9, 0.2, 0.8]},
        ),
        (
            pd.DataFrame(data={"col": ["a", "b", "b", "a", "b"], "prob": [0.1, 0.1, 0.1, 0.8, 0.2]}),
            "col",
            "prob",
            ["a", "b"],
            "a",
            {"a": [0.1, 0.1, 0.1, 0.8, 0.2], "b": [0.9, 0.9, 0.9, 0.2, 0.8]},
        ),
    ),
)
def test_get_prediction_data(dataframe, target, prediction, target_names, pos_label, expected):
    data = get_prediction_data(
        dataframe,
        DatasetColumns(
            utility_columns=DatasetUtilityColumns(target=target, prediction=prediction),
            target_names=target_names,
            num_feature_names=[],
            cat_feature_names=[],
            text_feature_names=[],
            datetime_feature_names=[],
        ),
        pos_label=pos_label,
    )
    for label in target_names:
        assert np.allclose(data.prediction_probas[label], expected[label], atol=1e-6)
