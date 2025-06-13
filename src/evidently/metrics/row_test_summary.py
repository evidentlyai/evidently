from typing import List
from typing import Sequence

from evidently.core.container import MetricContainer
from evidently.core.container import MetricOrContainer
from evidently.core.report import Context
from evidently.metrics import MeanValue
from evidently.tests import gte


class RowTestSummary(MetricContainer):
    columns: List[str] = []
    min_success_rate: float = 1

    def generate_metrics(self, context: "Context") -> Sequence[MetricOrContainer]:
        test_columns = self.columns or context.data_definition.test_descriptors or []
        return [
            MeanValue(column=tc, tests=[gte(self.min_success_rate, alias=f"Share of passed '{tc}' row tests")])
            for tc in test_columns
        ]
