# ruff: noqa: E501
# fmt: off
from evidently.core.metric_types import MetricTest
from evidently.pydantic_utils import register_type_alias

register_type_alias(MetricTest, "evidently.metrics.column_statistics.ValueDriftTest", "evidently:test_v2:ValueDriftTest")
register_type_alias(MetricTest, "evidently.tests.categorical_tests.IsInMetricTest", "evidently:test_v2:IsInMetricTest")
register_type_alias(MetricTest, "evidently.tests.categorical_tests.NotInMetricTest", "evidently:test_v2:NotInMetricTest")
register_type_alias(MetricTest, "evidently.tests.numerical_tests.ComparisonTest", "evidently:test_v2:ComparisonTest")
register_type_alias(MetricTest, "evidently.tests.numerical_tests.EqualMetricTest", "evidently:test_v2:EqualMetricTest")
register_type_alias(MetricTest, "evidently.tests.numerical_tests.EqualMetricTestBase", "evidently:test_v2:EqualMetricTestBase")
register_type_alias(MetricTest, "evidently.tests.numerical_tests.GreaterOrEqualMetricTest", "evidently:test_v2:GreaterOrEqualMetricTest")
register_type_alias(MetricTest, "evidently.tests.numerical_tests.GreaterThanMetricTest", "evidently:test_v2:GreaterThanMetricTest")
register_type_alias(MetricTest, "evidently.tests.numerical_tests.LessOrEqualMetricTest", "evidently:test_v2:LessOrEqualMetricTest")
register_type_alias(MetricTest, "evidently.tests.numerical_tests.LessThanMetricTest", "evidently:test_v2:LessThanMetricTest")
register_type_alias(MetricTest, "evidently.tests.numerical_tests.NotEqualMetricTest", "evidently:test_v2:NotEqualMetricTest")
