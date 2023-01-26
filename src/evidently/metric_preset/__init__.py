from .classification_performance import ClassificationPreset
from .data_drift import DataDriftPreset
from .data_quality import DataQualityPreset
from .regression_performance import RegressionPreset
from .target_drift import TargetDriftPreset
from .text_overview import TextOverviewPreset

__all__ = [
    ClassificationPreset.__name__,
    DataDriftPreset.__name__,
    DataQualityPreset.__name__,
    RegressionPreset.__name__,
    TargetDriftPreset.__name__,
    TextOverviewPreset.__name__,
]
