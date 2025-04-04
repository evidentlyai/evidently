# ruff: noqa: E501
# fmt: off
from evidently.core.metric_types import MetricResult
from evidently.pydantic_utils import register_type_alias

register_type_alias(MetricResult, "evidently.core.metric_types.ByLabelCountValue", "evidently:metric_result_v2:ByLabelCountValue")
register_type_alias(MetricResult, "evidently.core.metric_types.ByLabelValue", "evidently:metric_result_v2:ByLabelValue")
register_type_alias(MetricResult, "evidently.core.metric_types.CountValue", "evidently:metric_result_v2:CountValue")
register_type_alias(MetricResult, "evidently.core.metric_types.MeanStdValue", "evidently:metric_result_v2:MeanStdValue")
register_type_alias(MetricResult, "evidently.core.metric_types.SingleValue", "evidently:metric_result_v2:SingleValue")
