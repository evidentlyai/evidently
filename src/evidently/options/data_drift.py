from dataclasses import dataclass
from typing import Optional, Dict, Callable, Union


DEFAULT_CONFIDENCE = 0.95
DEFAULT_NBINSX = 10


@dataclass
class DataDriftOptions:
    confidence: Union[float, Dict[str, float]] = DEFAULT_CONFIDENCE
    drift_share: float = 0.5
    nbinsx: Union[int, Dict[str, int]] = DEFAULT_NBINSX
    xbins: Optional[Dict[str, int]] = None
    feature_stattest_func: Union[None, Callable, Dict[str, Callable]] = None
    cat_target_stattest_func: Optional[Callable] = None
    num_target_stattest_func: Optional[Callable] = None

    def as_dict(self):
        return {
            "confidence": self.confidence,
            "drift_share": self.drift_share,
            "nbinsx": self.nbinsx,
            "xbins": self.xbins
        }

    def get_confidence(self, feature_name: str) -> float:
        if isinstance(self.confidence, float):
            return self.confidence
        if isinstance(self.confidence, dict):
            return self.confidence.get(feature_name, DEFAULT_CONFIDENCE)
        raise ValueError(f"DataDriftOptions.confidence is incorrect type {type(self.confidence)}")

    def get_nbinsx(self, feature_name: str) -> int:
        if isinstance(self.nbinsx, int):
            return self.nbinsx
        if isinstance(self.nbinsx, dict):
            return self.nbinsx.get(feature_name, DEFAULT_NBINSX)
        raise ValueError(f"DataDriftOptions.nbinsx is incorrect type {type(self.nbinsx)}")

    def get_feature_stattest_func(self, feature_name: str, default: Callable) -> Callable:
        if callable(self.feature_stattest_func):
            return self.feature_stattest_func
        if isinstance(self.feature_stattest_func, dict):
            return self.feature_stattest_func.get(feature_name, default)
        return default
