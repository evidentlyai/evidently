import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer

from evidently.metric_preset import ClassificationPreset
from evidently.report import Report


def test_report_loading():
    dataset = load_breast_cancer(as_frame=True)

    ref = pd.DataFrame(dataset["target"])
    curr = pd.DataFrame(dataset["target"])

    ref["prediction"] = [np.random.random() for i in range(ref.shape[0])]
    curr["prediction"] = [np.random.random() for i in range(curr.shape[0])]

    report = Report(metrics=[ClassificationPreset(probas_threshold=0.7)])

    report.run(reference_data=ref, current_data=curr)

    report.save_profile("profile.json")

    report2 = Report.load_profile("profile.json")

    assert report.as_dict() == report2.as_dict()
