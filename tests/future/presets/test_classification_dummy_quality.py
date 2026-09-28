import pandas as pd
import pytest

from evidently.core.datasets import BinaryClassification
from evidently.core.datasets import DataDefinition
from evidently.core.datasets import Dataset
from evidently.core.report import Report
from evidently.metrics import DummyF1Score
from evidently.metrics import DummyPrecision
from evidently.metrics import DummyRecall
from evidently.presets import ClassificationDummyQuality


def _values(report: Report, dataset: Dataset):
    return [metric["value"] for metric in report.run(dataset).dict()["metrics"]]


@pytest.mark.parametrize(
    "classification_name,probas_threshold",
    [
        ("default", 0.9),
        ("named", None),
        ("named", 0.9),
    ],
)
def test_classification_dummy_quality_uses_preset_parameters(classification_name, probas_threshold):
    data = pd.DataFrame(
        data={
            "target": [0, 1, 1, 0, 1, 1],
            "prediction": [0.1, 0.9, 0.6, 0.4, 0.7, 0.2],
        }
    )
    definition = DataDefinition(
        classification=[
            BinaryClassification(target="target", prediction_probas="prediction", name=classification_name)
        ],
    )
    dataset = Dataset.from_pandas(data, data_definition=definition)
    params = dict(classification_name=classification_name, probas_threshold=probas_threshold)
    expected = _values(Report([DummyPrecision(**params), DummyRecall(**params), DummyF1Score(**params)]), dataset)

    assert _values(Report([ClassificationDummyQuality(**params)]), dataset) == pytest.approx(expected)
