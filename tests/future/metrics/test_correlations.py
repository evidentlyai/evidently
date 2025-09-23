import numpy as np
import pandas as pd

from evidently import BinaryClassification
from evidently import DataDefinition
from evidently import Dataset
from evidently import Report
from evidently.core.metric_types import DataframeValue
from evidently.metrics import ColumnCorrelationMatrix
from evidently.metrics import ColumnCorrelations
from evidently.metrics.data_quality import CorrelationMatrix


def test_column_correlations():
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    ds = Dataset.from_pandas(df)

    metric = ColumnCorrelations(column_name="a")
    report = Report(metrics=[metric])

    run = report.run(ds)

    result = run.context.get_metric_result(ColumnCorrelationMatrix(column_name="a", kind="cramer_v"))
    assert isinstance(result, DataframeValue)
    pd.testing.assert_frame_equal(result.value, pd.DataFrame([{"kind": "cramer_v", "column_name": "b", "value": 1.0}]))


def test_dataset_correlations():
    df = pd.DataFrame(
        {
            "my_target": [1, np.nan, 3] * 1000,
            "my_prediction": [1, 2, np.nan] * 1000,
            "feature_1": [1, 2, 3] * 1000,
            "feature_2": ["a", np.nan, "a"] * 1000,
        }
    )
    ds = Dataset.from_pandas(
        df,
        data_definition=DataDefinition(
            classification=[BinaryClassification(target="my_target", prediction_labels="my_prediction")]
        ),
    )

    metric = CorrelationMatrix()
    report = Report(metrics=[metric])

    run = report.run(ds)

    result = run.context.get_metric_result(metric)
    assert isinstance(result, DataframeValue)
    pd.testing.assert_frame_equal(
        result.value,
        pd.DataFrame(
            [{"my_target": 1, "my_prediction": np.nan}, {"my_target": np.nan, "my_prediction": 1}],
            index=["my_target", "my_prediction"],
        ),
    )
