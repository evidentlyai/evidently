# ruff: noqa: E501
# fmt: off
from evidently.legacy.metric_preset.metric_preset import MetricPreset
from evidently.pydantic_utils import register_type_alias

register_type_alias(MetricPreset, "evidently.legacy.metric_preset.classification_performance.ClassificationPreset", "evidently:metric_preset:ClassificationPreset")
register_type_alias(MetricPreset, "evidently.legacy.metric_preset.data_drift.DataDriftPreset", "evidently:metric_preset:DataDriftPreset")
register_type_alias(MetricPreset, "evidently.legacy.metric_preset.data_quality.DataQualityPreset", "evidently:metric_preset:DataQualityPreset")
register_type_alias(MetricPreset, "evidently.legacy.metric_preset.recsys.RecsysPreset", "evidently:metric_preset:RecsysPreset")
register_type_alias(MetricPreset, "evidently.legacy.metric_preset.regression_performance.RegressionPreset", "evidently:metric_preset:RegressionPreset")
register_type_alias(MetricPreset, "evidently.legacy.metric_preset.target_drift.TargetDriftPreset", "evidently:metric_preset:TargetDriftPreset")
register_type_alias(MetricPreset, "evidently.legacy.metric_preset.text_evals.TextEvals", "evidently:metric_preset:TextEvals")
