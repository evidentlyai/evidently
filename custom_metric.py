from evidently.core.metric_types import SingleValueMetric
from evidently.pydantic_utils import register_type_alias

class CustomAverageMetric(SingleValueMetric):
    class Config:
        type_alias = "evidently:metric_v2:CustomAverageMetric"
    column: str

register_type_alias(
    SingleValueMetric,
    "custom_metric.CustomAverageMetric",
    "evidently:metric_v2:CustomAverageMetric"
)