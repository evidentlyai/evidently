from evidently.pydantic_utils import register_type_alias
from evidently.v2.metrics.base import MetricConfig

register_type_alias(
    MetricConfig, "evidently.v2.metrics.base.ColumnMetricConfig", "evidently:metric_config:ColumnMetricConfig"
)
register_type_alias(
    MetricConfig, "evidently.v2.metrics.column_summary.ColumnMaxConfig", "evidently:metric_config:ColumnMaxConfig"
)
