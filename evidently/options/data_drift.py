from dataclasses import dataclass
from typing import Optional, Dict, Callable, Union


@dataclass
class DataDriftOptions:
    confidence: Union[float, Dict[str, float]] = 0.95
    drift_share: float = 0.5
    nbinsx: Optional[Dict[str, int]] = None
    xbins: Optional[Dict[str, int]] = None
    stattest_func: Optional[Callable] = None
    feature_stattest_func: Optional[Dict[str, Callable]] = None
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
            return self.confidence.get(feature_name, DataDriftOptions.confidence)
        raise ValueError(f"DataDriftOptions.confidence is incorrect type {type(self.confidence)}")

    def get_feature_stattest_func(self, feature_name: str, default: Callable) -> Callable:
        _default = default if self.stattest_func is None else self.stattest_func
        if self.feature_stattest_func is not None:
            return self.feature_stattest_func.get(feature_name, _default)
        return _default
