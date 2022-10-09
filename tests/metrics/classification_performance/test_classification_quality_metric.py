import numpy as np
import pandas as pd

from evidently import ColumnMapping
from evidently.metrics.base_metric import InputData
from evidently.metrics.classification_performance.classification_quality_metric import ClassificationQuality


def test_classification_quality():
    current = pd.DataFrame(data=dict(target=["a", "a", "a", "b", "b", "b", "c", "c", "c"],
                                     prediction=["a", "b", "c", "a", "b", "c", "a", "b", "c"]))

    metric = ClassificationQuality()
    results = metric.calculate(data=InputData(None, current, ColumnMapping()))
    assert np.isclose(results.current.accuracy, 0.333333)
    assert np.isclose(results.current.f1, 0.333333)
    assert np.isclose(results.current.precision, 0.333333)
    assert np.isclose(results.current.recall, 0.333333)
