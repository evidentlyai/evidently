import pandas as pd

from evidently import DataDefinition
from evidently import Dataset
from evidently import Regression
from evidently import Report
from evidently.metrics import MeanError
from evidently.tests import lte


def _run(metric):
    data = pd.DataFrame({"target": [1.0, 2.0, 3.0, 4.0], "prediction": [1.1, 2.2, 2.7, 4.4]})
    dataset = Dataset.from_pandas(data, data_definition=DataDefinition(regression=[Regression()]))
    return Report([metric], include_tests=True).run(dataset, None).dict()["tests"]


def test_std_tests_only_are_bound():
    tests = _run(MeanError(std_tests=[lte(0.0001)]))
    assert [t["name"] for t in tests] == ["Std Error: Less or Equal 0.000"]


def test_mean_tests_only_are_bound():
    tests = _run(MeanError(mean_tests=[lte(0.0001)]))
    assert [t["name"] for t in tests] == ["Mean Error: Less or Equal 0.000"]
