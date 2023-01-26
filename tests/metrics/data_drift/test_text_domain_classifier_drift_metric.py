import json

import pandas as pd
from pytest import approx
from sklearn.datasets import fetch_20newsgroups

from evidently.metrics.data_drift.text_domain_classifier_drift_metric import TextDomainClassifierDriftMetric
from evidently.report import Report


def test_text_domain_classifier_drift_metric():
    categories_ref = ["alt.atheism", "talk.religion.misc"]
    categories_cur = ["comp.graphics", "sci.space"]
    reference = fetch_20newsgroups(subset="train", remove=("headers", "footers", "quotes"), categories=categories_ref)
    current = fetch_20newsgroups(subset="test", remove=("headers", "footers", "quotes"), categories=categories_cur)
    reference_data = pd.DataFrame({"text": reference.data})
    current_data = pd.DataFrame({"text": current.data})

    report = Report(metrics=[TextDomainClassifierDriftMetric(text_column_name="text")])
    report.run(current_data=current_data, reference_data=reference_data)
    assert report.show()
    result_json = report.json()
    result = json.loads(result_json)["metrics"][0]["result"]

    assert result["text_column_name"] == "text"
    assert result["domain_classifier_roc_auc"] == approx(0.91, abs=0.02)
    assert result["random_classifier_95_percentile"] == approx(0.53, abs=0.01)
    assert result["content_drift"]
