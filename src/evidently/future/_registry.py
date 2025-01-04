from evidently.future.metric_types import Metric
from evidently.future.metric_types import MetricTest
from evidently.pydantic_utils import register_type_alias

register_type_alias(Metric, "evidently.future.backport.TestsConfig", "evidently:metric_v2:TestsConfig")
register_type_alias(Metric, "evidently.future.metric_types.ByLabelMetric", "evidently:metric_v2:ByLabelMetric")
register_type_alias(Metric, "evidently.future.metric_types.CountMetric", "evidently:metric_v2:CountMetric")
register_type_alias(Metric, "evidently.future.metric_types.SingleValueMetric", "evidently:metric_v2:SingleValueMetric")
register_type_alias(
    Metric, "evidently.future.metrics.column_statistics.CategoryCount", "evidently:metric_v2:CategoryCount"
)
register_type_alias(
    Metric, "evidently.future.metrics.column_statistics.InListValueCount", "evidently:metric_v2:InListValueCount"
)
register_type_alias(
    Metric, "evidently.future.metrics.column_statistics.InRangeValueCount", "evidently:metric_v2:InRangeValueCount"
)
register_type_alias(Metric, "evidently.future.metrics.column_statistics.MaxValue", "evidently:metric_v2:MaxValue")
register_type_alias(Metric, "evidently.future.metrics.column_statistics.MeanValue", "evidently:metric_v2:MeanValue")
register_type_alias(Metric, "evidently.future.metrics.column_statistics.MedianValue", "evidently:metric_v2:MedianValue")
register_type_alias(Metric, "evidently.future.metrics.column_statistics.MinValue", "evidently:metric_v2:MinValue")
register_type_alias(
    Metric, "evidently.future.metrics.column_statistics.MissingValueCount", "evidently:metric_v2:MissingValueCount"
)
register_type_alias(
    Metric, "evidently.future.metrics.column_statistics.OutListValueCount", "evidently:metric_v2:OutListValueCount"
)
register_type_alias(
    Metric, "evidently.future.metrics.column_statistics.OutRangeValueCount", "evidently:metric_v2:OutRangeValueCount"
)
register_type_alias(
    Metric, "evidently.future.metrics.column_statistics.QuantileValue", "evidently:metric_v2:QuantileValue"
)
register_type_alias(
    Metric, "evidently.future.metrics.column_statistics.StatisticsMetric", "evidently:metric_v2:StatisticsMetric"
)
register_type_alias(Metric, "evidently.future.metrics.column_statistics.StdValue", "evidently:metric_v2:StdValue")
register_type_alias(Metric, "evidently.future.metrics.data_quality.F1Metric", "evidently:metric_v2:F1Metric")
register_type_alias(
    Metric, "evidently.future.metrics.data_quality.PrecisionMetric", "evidently:metric_v2:PrecisionMetric"
)
register_type_alias(Metric, "evidently.future.metrics.data_quality.RecallMetric", "evidently:metric_v2:RecallMetric")
register_type_alias(Metric, "evidently.future.metrics.data_quality.RocAucMetric", "evidently:metric_v2:RocAucMetric")
register_type_alias(
    Metric, "evidently.future.metrics.dataset_statistics.ColumnCount", "evidently:metric_v2:ColumnCount"
)
register_type_alias(Metric, "evidently.future.metrics.dataset_statistics.RowCount", "evidently:metric_v2:RowCount")
register_type_alias(Metric, "evidently.future.metrics.group_by.GroupByMetric", "evidently:metric_v2:GroupByMetric")
register_type_alias(
    MetricTest, "evidently.future.tests.categorical_tests.IsInMetricTest", "evidently:test_config:IsInMetricTest"
)
register_type_alias(
    MetricTest, "evidently.future.tests.categorical_tests.NotInMetricTest", "evidently:test_config:NotInMetricTest"
)
register_type_alias(
    MetricTest, "evidently.future.tests.numerical_tests.ComparisonTest", "evidently:test_config:ComparisonTest"
)
register_type_alias(
    MetricTest, "evidently.future.tests.numerical_tests.EqualMetricTest", "evidently:test_config:EqualMetricTest"
)
register_type_alias(
    MetricTest,
    "evidently.future.tests.numerical_tests.GreaterOrEqualMetricTest",
    "evidently:test_config:GreaterOrEqualMetricTest",
)
register_type_alias(
    MetricTest,
    "evidently.future.tests.numerical_tests.GreaterThanMetricTest",
    "evidently:test_config:GreaterThanMetricTest",
)
register_type_alias(
    MetricTest,
    "evidently.future.tests.numerical_tests.LessOrEqualMetricTest",
    "evidently:test_config:LessOrEqualMetricTest",
)
register_type_alias(
    MetricTest, "evidently.future.tests.numerical_tests.LessThanMetricTest", "evidently:test_config:LessThanMetricTest"
)
