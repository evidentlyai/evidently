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

    def get_confidence(self, feature_name):
        if isinstance(self.confidence, float):
            return self.confidence
        if isinstance(self.confidence, dict):
            return self.confidence.get(feature_name, DataDriftOptions.confidence)
        raise ValueError(f"DataDriftOptions.confidence is incorrect type {type(self.confidence)}")
