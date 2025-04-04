# ruff: noqa: E501
# fmt: off
from evidently.core.metric_types import BoundTest
from evidently.pydantic_utils import register_type_alias

register_type_alias(BoundTest, "evidently.core.metric_types.ByLabelBoundTest", "evidently:bound_test:ByLabelBoundTest")
register_type_alias(BoundTest, "evidently.core.metric_types.ByLabelCountBoundTest", "evidently:bound_test:ByLabelCountBoundTest")
register_type_alias(BoundTest, "evidently.core.metric_types.CountBoundTest", "evidently:bound_test:CountBoundTest")
register_type_alias(BoundTest, "evidently.core.metric_types.MeanStdBoundTest", "evidently:bound_test:MeanStdBoundTest")
register_type_alias(BoundTest, "evidently.core.metric_types.SingleValueBoundTest", "evidently:bound_test:SingleValueBoundTest")
register_type_alias(BoundTest, "evidently.metrics.column_statistics.ValueDriftBoundTest", "evidently:bound_test:ValueDriftBoundTest")
