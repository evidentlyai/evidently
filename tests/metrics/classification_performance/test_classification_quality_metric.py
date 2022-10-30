import numpy as np
import pandas as pd

from evidently import ColumnMapping
from evidently.metrics import ClassificationQualityMetric
from evidently.report import Report


def test_classification_quality():
    current = pd.DataFrame(
        data=dict(
            target=["a", "a", "a", "b", "b", "b", "c", "c", "c"],
            prediction=["a", "b", "c", "a", "b", "c", "a", "b", "c"],
        ),
    )

    metric = ClassificationQualityMetric()
    report = Report(metrics=[metric])
    report.run(reference_data=None, current_data=current, column_mapping=ColumnMapping())

    results = metric.get_result()
    assert np.isclose(results.current.accuracy, 0.333333)
    assert np.isclose(results.current.f1, 0.333333)
    assert np.isclose(results.current.precision, 0.333333)
    assert np.isclose(results.current.recall, 0.333333)


def test_classification_quality_binary():
    current = pd.DataFrame(
        data=dict(
            target=[1, 1, 1, 1, 0, 0, 0, 0, 1],
            prediction=[0.7, 0.8, 0.9, 0.4, 0.1, 0.2, 0.1, 0.3, 0.8],
        ),
    )

    metric = ClassificationQualityMetric()
    report = Report(metrics=[metric])
    report.run(reference_data=None, current_data=current, column_mapping=ColumnMapping())

    results = metric.get_result()
    assert np.isclose(results.current.accuracy, 8 / 9)
    assert np.isclose(results.current.f1, 0.888888888888889)
    assert np.isclose(results.current.precision, 4 / 4)
    assert np.isclose(results.current.recall, 4 / 5)
    assert np.isclose(results.current.roc_auc, 1.0)
    assert np.isclose(results.current.log_loss, 0.29057)
    assert np.isclose(results.current.tpr, 1.0)
    assert np.isclose(results.current.tnr, 0.8)
    assert np.isclose(results.current.fpr, 0.2)
    assert np.isclose(results.current.fnr, 0.0)
