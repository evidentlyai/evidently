import warnings

from .monitoring import ModelMonitoring
from .monitors.cat_target_drift import CatTargetDriftMonitor
from .monitors.classification_performance import ClassificationPerformanceMonitor
from .monitors.data_drift import DataDriftMonitor
from .monitors.data_quality import DataQualityMonitor
from .monitors.num_target_drift import NumTargetDriftMonitor
from .monitors.prob_classification_performance import ProbClassificationPerformanceMonitor
from .monitors.regression_performance import RegressionPerformanceMonitor

warnings.warn("model monitoring is deprecated, use metrics instead")
