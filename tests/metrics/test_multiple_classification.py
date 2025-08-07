import pandas as pd

from evidently import BinaryClassification
from evidently import DataDefinition
from evidently import Dataset
from evidently import Report
from evidently.presets import ClassificationQuality


def test_multiple_classification():
    data = pd.DataFrame(
        data={
            "a1": ["a", "b", "a", "b"],
            "predict1": ["a", "b", "a", "b"],
            "predict2": [0.1, 0.7, 0.1, 0.8],
            "predict3": [0.8, 0.7, 0.1, 0.8],
        }
    )

    report = Report(
        [ClassificationQuality("c1")],
    )

    dataset = Dataset.from_pandas(
        data,
        DataDefinition(
            classification=[
                BinaryClassification(name="c1", target="a1", prediction_labels="predict1", pos_label="b"),
                BinaryClassification(name="c2", target="a1", prediction_labels="predict2", pos_label="b"),
                BinaryClassification(name="c3", target="a1", prediction_labels="predict3", pos_label="b"),
            ]
        ),
    )
    run1 = report.run(dataset)

    run2 = Report([ClassificationQuality("c3")]).run(dataset)
    run3 = Report([ClassificationQuality("c1"), ClassificationQuality("c3")]).run(dataset)

    assert run1.dict()["metrics"] + run2.dict()["metrics"] == run3.dict()["metrics"]
