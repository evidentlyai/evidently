"""Predefined Test Presets for Test Suite"""
from .classification_binary import BinaryClassificationTestPreset
from .classification_binary_topk import BinaryClassificationTopKTestPreset
from .classification_multiclass import MulticlassClassificationTestPreset
from .data_drift import DataDriftTestPreset
from .data_quality import DataQualityTestPreset
from .data_stability import DataStabilityTestPreset
from .no_target_performance import NoTargetPerformanceTestPreset
from .regression import RegressionTestPreset

__all__ = [
    BinaryClassificationTestPreset.__name__,
    BinaryClassificationTopKTestPreset.__name__,
    MulticlassClassificationTestPreset.__name__,
    DataDriftTestPreset.__name__,
    DataQualityTestPreset.__name__,
    DataStabilityTestPreset.__name__,
    NoTargetPerformanceTestPreset.__name__,
    RegressionTestPreset.__name__,
]
