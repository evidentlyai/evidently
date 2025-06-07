from typing import Sequence

from evidently.core.container import MetricContainer
from evidently.core.container import MetricOrContainer
from evidently.core.report import Context
from evidently.metrics import MeanValue
from evidently.tests import eq


class ColumnTests(MetricContainer):
    def generate_metrics(self, context: "Context") -> Sequence[MetricOrContainer]:
        test_columns = context.data_definition.test_descriptors or []
        return [MeanValue(column=tc, tests=[eq(1, alias="Passed for all rows")]) for tc in test_columns]
