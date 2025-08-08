# ruff: noqa: E501
# fmt: off
from evidently.core.container import MetricContainer
from evidently.pydantic_utils import register_type_alias

register_type_alias(MetricContainer, "evidently.core.container.ColumnMetricContainer", "evidently:metric_container:ColumnMetricContainer")
register_type_alias(MetricContainer, "evidently.generators.column.ColumnMetricGenerator", "evidently:metric_container:ColumnMetricGenerator")
register_type_alias(MetricContainer, "evidently.metrics.group_by.GroupBy", "evidently:metric_container:GroupBy")
register_type_alias(MetricContainer, "evidently.presets.classification.ClassificationDummyQuality", "evidently:metric_container:ClassificationDummyQuality")
register_type_alias(MetricContainer, "evidently.presets.classification.ClassificationPreset", "evidently:metric_container:ClassificationPreset")
register_type_alias(MetricContainer, "evidently.presets.classification.ClassificationQuality", "evidently:metric_container:ClassificationQuality")
register_type_alias(MetricContainer, "evidently.presets.classification.ClassificationQualityByLabel", "evidently:metric_container:ClassificationQualityByLabel")
register_type_alias(MetricContainer, "evidently.presets.dataset_stats.DataSummaryPreset", "evidently:metric_container:DataSummaryPreset")
register_type_alias(MetricContainer, "evidently.presets.dataset_stats.DatasetStats", "evidently:metric_container:DatasetStats")
register_type_alias(MetricContainer, "evidently.presets.dataset_stats.TextEvals", "evidently:metric_container:TextEvals")
register_type_alias(MetricContainer, "evidently.presets.dataset_stats.ValueStats", "evidently:metric_container:ValueStats")
register_type_alias(MetricContainer, "evidently.presets.drift.DataDriftPreset", "evidently:metric_container:DataDriftPreset")
register_type_alias(MetricContainer, "evidently.presets.regression.RegressionDummyQuality", "evidently:metric_container:RegressionDummyQuality")
register_type_alias(MetricContainer, "evidently.presets.regression.RegressionPreset", "evidently:metric_container:RegressionPreset")
register_type_alias(MetricContainer, "evidently.presets.regression.RegressionQuality", "evidently:metric_container:RegressionQuality")
register_type_alias(MetricContainer, "evidently.metrics.row_test_summary.RowTestSummary", "evidently:metric_container:RowTestSummary")

register_type_alias(MetricContainer, "evidently.presets.special.TestSummaryInfoPreset", "evidently:metric_container:TestSummaryInfoPreset")
