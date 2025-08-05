from typing import Optional
from typing import Sequence
from typing import Type

import pytest

from evidently.core.datasets import Dataset
from evidently.core.metric_types import BoundTest
from evidently.core.metric_types import Metric
from evidently.core.metric_types import SingleValueCalculation
from evidently.core.metric_types import SingleValueMetric
from evidently.core.metric_types import TestStatus
from evidently.core.metric_types import TMetricResult
from evidently.core.report import Context
from evidently.core.report import Report
from evidently.core.tests import GenericTest
from evidently.tests import eq
from evidently.tests import gt
from evidently.tests import lt
from evidently.tests import not_eq


class StubMetric(SingleValueMetric):
    def get_bound_tests(self, context: "Context") -> Sequence[BoundTest]:
        return []


class StubMetricCalculation(SingleValueCalculation[StubMetric]):
    def calculate(self, context: "Context", current_data: Dataset, reference_data: Optional[Dataset]) -> TMetricResult:
        pass

    def display_name(self) -> str:
        return "Stub metric"

    def to_metric(self) -> "Metric":
        return StubMetric()


@pytest.mark.parametrize(
    "test,value,expected_metric,expected_descriptor",
    [
        (eq(1), 1, TestStatus.SUCCESS, True),
        (not_eq(1), 1, TestStatus.FAIL, False),
        (gt(1), 2, TestStatus.SUCCESS, True),
        (lt(1), 0, TestStatus.SUCCESS, True),
        (eq("a"), "a", None, True),
        (not_eq("a"), "a", None, False),
    ],
)
def test_instances(test: GenericTest, value, expected_metric, expected_descriptor):
    if expected_metric is None:
        assert test.metric is None
    else:
        calculation = StubMetricCalculation("stub_metric", StubMetric())
        assert test.metric.run(Context(Report([])), calculation, calculation.result(value)).status == expected_metric
    if expected_descriptor is None:
        assert test.descriptor is None
    else:
        assert test.descriptor.condition.check(value) == expected_descriptor


@pytest.mark.parametrize("test,args", [(lt, ("a",))])
def test_failed_instances(test: Type, args):
    with pytest.raises(ValueError):
        test(*args)
