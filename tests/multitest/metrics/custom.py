import pandas as pd

from evidently.base_metric import InputData
from evidently.metrics.custom_metric import CustomValueMetric
from tests.multitest.conftest import AssertResultFields
from tests.multitest.datasets import TestDataset
from tests.multitest.metrics.conftest import TestMetric
from tests.multitest.metrics.conftest import metric


def custom_func(data: InputData) -> float:
    return 0.3


@metric
def custom_callable_metric():
    reference_data = current_data = pd.DataFrame({"text": [1, 2, 3]})

    return TestMetric(
        "custom_callable_metric",
        CustomValueMetric(func=custom_func, title="aaa"),
        AssertResultFields({"value": 0.3}),
        datasets=[
            TestDataset("custom_callable_metric_data", current=current_data, reference=reference_data, tags=[]),
        ],
    )
