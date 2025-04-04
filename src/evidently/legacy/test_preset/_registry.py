# ruff: noqa: E501
# fmt: off
from evidently.legacy.test_preset.test_preset import TestPreset
from evidently.pydantic_utils import register_type_alias

register_type_alias(TestPreset, "evidently.legacy.test_preset.classification_binary.BinaryClassificationTestPreset", "evidently:test_preset:BinaryClassificationTestPreset")
register_type_alias(TestPreset, "evidently.legacy.test_preset.classification_binary_topk.BinaryClassificationTopKTestPreset", "evidently:test_preset:BinaryClassificationTopKTestPreset")
register_type_alias(TestPreset, "evidently.legacy.test_preset.classification_multiclass.MulticlassClassificationTestPreset", "evidently:test_preset:MulticlassClassificationTestPreset")
register_type_alias(TestPreset, "evidently.legacy.test_preset.data_drift.DataDriftTestPreset", "evidently:test_preset:DataDriftTestPreset")
register_type_alias(TestPreset, "evidently.legacy.test_preset.data_quality.DataQualityTestPreset", "evidently:test_preset:DataQualityTestPreset")
register_type_alias(TestPreset, "evidently.legacy.test_preset.data_stability.DataStabilityTestPreset", "evidently:test_preset:DataStabilityTestPreset")
register_type_alias(TestPreset, "evidently.legacy.test_preset.no_target_performance.NoTargetPerformanceTestPreset", "evidently:test_preset:NoTargetPerformanceTestPreset")
register_type_alias(TestPreset, "evidently.legacy.test_preset.recsys.RecsysTestPreset", "evidently:test_preset:RecsysTestPreset")
register_type_alias(TestPreset, "evidently.legacy.test_preset.regression.RegressionTestPreset", "evidently:test_preset:RegressionTestPreset")
