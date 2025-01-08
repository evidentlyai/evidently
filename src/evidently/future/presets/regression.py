from typing import Dict
from typing import List

from evidently.future.container import MetricContainer
from evidently.future.metric_types import Metric
from evidently.future.metric_types import MetricId
from evidently.future.metric_types import MetricResult
from evidently.future.metrics import MAE
from evidently.future.metrics import MAPE
from evidently.future.metrics import AbsMaxError
from evidently.future.metrics import MeanError
from evidently.future.metrics import R2Score
from evidently.future.report import Context
from evidently.metrics import RegressionQualityMetric
from evidently.model.widget import BaseWidgetInfo


class RegressionQuality(MetricContainer):
    def generate_metrics(self, context: Context) -> List[Metric]:
        return [
            MeanError(),
            MAPE(),
            MAE(),
            R2Score(),
            AbsMaxError(),
        ]

    def render(self, context: Context, results: Dict[MetricId, MetricResult]) -> List[BaseWidgetInfo]:
        return context.get_legacy_metric(RegressionQualityMetric())[1]
