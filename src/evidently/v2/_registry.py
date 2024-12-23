from evidently.pydantic_utils import register_type_alias
from evidently.v2.metrics import Metric

register_type_alias(Metric, "evidently.v2.metrics.data_quality.F1Metric", "evidently:metric_v2:F1Metric")
register_type_alias(Metric, "evidently.v2.metrics.data_quality.PrecisionMetric", "evidently:metric_v2:PrecisionMetric")
register_type_alias(Metric, "evidently.v2.metrics.data_quality.RecallMetric", "evidently:metric_v2:RecallMetric")
register_type_alias(Metric, "evidently.v2.metrics.data_quality.RocAucMetric", "evidently:metric_v2:RocAucMetric")
register_type_alias(Metric, "evidently.v2.metrics.group_by.GroupByMetric", "evidently:metric_v2:GroupByMetric")
register_type_alias(Metric, "evidently.v2.metrics.max.ColumnMax", "evidently:metric_v2:ColumnMax")
register_type_alias(Metric, "evidently.v2.metrics.mean.ColumnMean", "evidently:metric_v2:ColumnMean")
register_type_alias(Metric, "evidently.v2.metrics.min.ColumnMin", "evidently:metric_v2:ColumnMin")
register_type_alias(Metric, "evidently.v2.metrics.quantile.ColumnQuantile", "evidently:metric_v2:ColumnQuantile")
