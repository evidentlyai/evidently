from typing import Dict
from typing import Optional
from typing import overload

from evidently.base_metric import MetricResultField
from evidently.metric_results import ScatterData


class PredActualScatter(MetricResultField):
    predicted: ScatterData
    actual: ScatterData


@overload
def scatter_as_dict(scatter: PredActualScatter) -> Dict[str, ScatterData]:
    ...


@overload
def scatter_as_dict(scatter: Optional[PredActualScatter]) -> Optional[Dict[str, ScatterData]]:
    ...


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
        # todo: will fail if data is not Series
        if isinstance(self.current, list) or isinstance(self.reference, list):
            return RegressionMetricScatter(
                current=[x * other for x in self.current],
                reference=[x * other for x in self.reference] if self.reference is not None else None,
            )
        return RegressionMetricScatter(
            current=self.current * other, reference=self.reference * other if self.reference is not None else None
        )


class RegressionMetricsScatter(MetricResultField):
    r2_score: RegressionMetricScatter
    rmse: RegressionMetricScatter
    mean_abs_error: RegressionMetricScatter
    mean_abs_perc_error: RegressionMetricScatter
