import pandas as pd

from evidently.legacy.base_metric import InputData
from evidently.legacy.metrics.custom_metric import CustomValueMetric
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
        name="custom_callable_metric",
        metric=CustomValueMetric(func=custom_func, title="aaa"),
        fingerprint="bf2e25a384e9d1ad621d73862c661a95",
        outcomes=AssertResultFields({"value": 0.3}),
        datasets=[
            TestDataset("custom_callable_metric_data", current=current_data, reference=reference_data, tags=[]),
        ],
    )
