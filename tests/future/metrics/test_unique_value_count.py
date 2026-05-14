import numpy as np
import pandas as pd

from evidently import DataDefinition
from evidently import Dataset
from evidently import Report
from evidently.core.metric_types import ByLabelCountValue
from evidently.metrics import UniqueValueCount


def test_unique_value_count_metric():
    metric = UniqueValueCount(column="col1")
    result = {
        "a": {
            "count": 3,
            "share": 0.75,
            "count_display_name": "Unique Value Count: col1 for label a",
            "share_display_name": "Unique Value Share: col1 for label a",
        },
        "b": {
            "count": 1,
            "share": 0.25,
            "count_display_name": "Unique Value Count: col1 for label b",
            "share_display_name": "Unique Value Share: col1 for label b",
        },
        "c": {
            "count": 0,
            "share": 0.0,
            "count_display_name": "Unique Value Count: col1 for label c",
            "share_display_name": "Unique Value Share: col1 for label c",
        },
    }
    data = pd.DataFrame({"col1": ["a", "a", "a", "b"]})
    dataset = Dataset.from_pandas(data)
    report = Report([metric])
    run = report.run(dataset, None)
    res = run._context.get_metric_result(metric)
    assert isinstance(res, ByLabelCountValue)
    for label in ["a", "b", "c"]:
        label_count, label_share = res.get_label_result(label)
        assert label_count.value == result[label]["count"]
        assert label_count.display_name == result[label]["count_display_name"]
        assert label_share.value == result[label]["share"]
        assert label_share.display_name == result[label]["share_display_name"]


def test_unique_value_count_with_pd_na_in_string_dtype():
    """Issue #1616: pd.NA in a nullable-string column must not become a label key."""
    metric = UniqueValueCount(column="col1")
    data = pd.DataFrame({"col1": pd.Series(["a", "a", "b", pd.NA], dtype="string")})
    dataset = Dataset.from_pandas(data, DataDefinition(categorical_columns=["col1"]))
    res = Report([metric]).run(dataset, None)._context.get_metric_result(metric)
    assert isinstance(res, ByLabelCountValue)
    assert set(res.labels()) == {"a", "b"}
    a_count, _ = res.get_label_result("a")
    b_count, _ = res.get_label_result("b")
    assert a_count.value == 2
    assert b_count.value == 1


def test_unique_value_count_with_nan_in_object_dtype():
    """np.nan / None in an object column also must not surface as a label."""
    metric = UniqueValueCount(column="col1")
    data = pd.DataFrame({"col1": pd.Series(["a", "b", None, np.nan], dtype="object")})
    dataset = Dataset.from_pandas(data, DataDefinition(categorical_columns=["col1"]))
    res = Report([metric]).run(dataset, None)._context.get_metric_result(metric)
    assert isinstance(res, ByLabelCountValue)
    assert set(res.labels()) == {"a", "b"}


def test_unique_value_count_with_pd_na_in_int64_dtype():
    """pd.NA in a nullable Int64 column."""
    metric = UniqueValueCount(column="col1")
    data = pd.DataFrame({"col1": pd.array([1, 2, 2, pd.NA], dtype="Int64")})
    dataset = Dataset.from_pandas(data, DataDefinition(categorical_columns=["col1"]))
    res = Report([metric]).run(dataset, None)._context.get_metric_result(metric)
    assert isinstance(res, ByLabelCountValue)
    assert set(res.labels()) == {1, 2}
