import pandas as pd

import pytest

from evidently.pipeline.column_mapping import ColumnMapping
from evidently.v2.metrics.base_metric import InputData
from evidently.v2.metrics.base_metric import Metric


def test_base_metrics_class() -> None:
    base_metric = Metric()

    with pytest.raises(NotImplementedError):
        base_metric.calculate(
            data=InputData(current_data=pd.DataFrame(), reference_data=None, column_mapping=ColumnMapping()
                           ), metrics={}
        )
