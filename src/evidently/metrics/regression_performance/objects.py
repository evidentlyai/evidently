from typing import Dict
from typing import Optional

from evidently.base_metric import MetricResultField
from evidently.objects import ScatterData


class PredActualScatter(MetricResultField):
    predicted: ScatterData
    actual: ScatterData


def scatter_as_dict(scatter: Optional[PredActualScatter]) -> Optional[Dict[str, ScatterData]]:
    if scatter is None:
        return None
    return scatter.dict()


class RegressionScatter(MetricResultField):
    underestimation: PredActualScatter
    majority: PredActualScatter
    overestimation: PredActualScatter


class RegressionMetricScatter(MetricResultField):
    current: ScatterData
    reference: Optional[ScatterData] = None

    def __mul__(self, other: float):
        return RegressionMetricScatter(
            current=self.current * other, reference=self.reference * other if self.reference is not None else None
        )


class RegressionMetricsScatter(MetricResultField):
    r2_score: RegressionMetricScatter
    rmse: RegressionMetricScatter
    mean_abs_error: RegressionMetricScatter
    mean_abs_perc_error: RegressionMetricScatter
