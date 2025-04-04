import numpy as np
import pandas as pd
import pytest
from sklearn.datasets import load_breast_cancer

from evidently.legacy.metric_preset import ClassificationPreset
from evidently.legacy.report import Report
from evidently.legacy.test_preset import BinaryClassificationTestPreset
from evidently.legacy.test_suite import TestSuite


@pytest.fixture
def data():
    dataset = load_breast_cancer(as_frame=True)

    ref = pd.DataFrame(dataset["target"])
    curr = pd.DataFrame(dataset["target"])

    ref["prediction"] = [np.random.random() for i in range(ref.shape[0])]
    curr["prediction"] = [np.random.random() for i in range(curr.shape[0])]
    return ref, curr


def test_report_loading(data):
    ref, curr = data

    report = Report(metrics=[ClassificationPreset(probas_threshold=0.7)])

    report.run(reference_data=ref, current_data=curr)

    report.save("profile.json")

    report2 = Report.load("profile.json")

    assert report2.as_dict() == report.as_dict()


def test_suite_loading(data):
    ref, curr = data

    ts = TestSuite([BinaryClassificationTestPreset()])

    ts.run(reference_data=ref, current_data=curr)
    ts._inner_suite.raise_for_error()
    ts.save("profile.json")

    ts2 = TestSuite.load("profile.json")

    assert ts2.as_dict() == ts.as_dict()
