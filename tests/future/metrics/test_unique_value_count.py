import pandas as pd

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
