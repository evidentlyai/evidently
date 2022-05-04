from dataclasses import dataclass
from typing import Optional, Dict, Union
import warnings

from evidently.analyzers.stattests import StatTest, PossibleStatTestType

DEFAULT_CONFIDENCE = 0.95
DEFAULT_THRESHOLD = 0.05
DEFAULT_NBINSX = 10


@dataclass
class DataDriftOptions:
    confidence: Optional[Union[float, Dict[str, float]]] = None
    threshold: Optional[Union[float, Dict[str, float]]] = None
    drift_share: float = 0.5
    nbinsx: Union[int, Dict[str, int]] = DEFAULT_NBINSX
    xbins: Optional[Dict[str, int]] = None

    feature_stattest_func: Optional[Union[PossibleStatTestType, Dict[str, PossibleStatTestType]]] = None

    stattest: Optional[PossibleStatTestType] = None
    cat_stattest: Optional[PossibleStatTestType] = None
    num_stattest: Optional[PossibleStatTestType] = None
    per_feature_stattest: Optional[Dict[str, PossibleStatTestType]] = None

    cat_target_stattest_func: Optional[PossibleStatTestType] = None
    num_target_stattest_func: Optional[PossibleStatTestType] = None

    def as_dict(self):
        return {
            "confidence": self.confidence,
            "drift_share": self.drift_share,
            "nbinsx": self.nbinsx,
            "xbins": self.xbins
        }

    def get_threshold(self, feature_name: str) -> float:
        if self.confidence is not None and self.threshold is not None:
            raise ValueError("Only DataDriftOptions.confidence or DataDriftOptions.threshold can be set")
        if self.confidence is not None:
            warnings.warn("DataDriftOptions.confidence is deprecated, use DataDriftOptions.threshold instead.")
            if isinstance(self.confidence, float):
                return 1. - self.confidence
            if isinstance(self.confidence, dict):
                return 1. - self.confidence.get(feature_name, DEFAULT_CONFIDENCE)
            raise ValueError(f"DataDriftOptions.confidence is incorrect type {type(self.confidence)}")
        if self.threshold is not None:
            if isinstance(self.threshold, float):
                return self.threshold
            if isinstance(self.threshold, dict):
                return self.threshold.get(feature_name, DEFAULT_THRESHOLD)
            raise ValueError(f"DataDriftOptions.threshold is incorrect type {type(self.threshold)}")
        return DEFAULT_THRESHOLD

    def get_nbinsx(self, feature_name: str) -> int:
        if isinstance(self.nbinsx, int):
            return self.nbinsx
        if isinstance(self.nbinsx, dict):
            return self.nbinsx.get(feature_name, DEFAULT_NBINSX)
        raise ValueError(f"DataDriftOptions.nbinsx is incorrect type {type(self.nbinsx)}")

    def get_feature_stattest_func(
            self,
            feature_name: str,
            feature_type: str,
            default: PossibleStatTestType) -> PossibleStatTestType:
        if self.feature_stattest_func is not None and any([self.stattest,
                                                           self.cat_stattest,
                                                           self.num_stattest,
                                                           self.per_feature_stattest]):
            raise ValueError("Cannot use DataDriftOptions.feature_stattest_func along with any "
                             "of DataDriftOptions.cat_stattest_func,"
                             " DataDriftOptions.num_stattest_func,"
                             " DataDriftOptions.per_feature_stattest_func.")
        if self.feature_stattest_func is not None:
            warnings.warn("DataDriftOptions.feature_stattest_func is deprecated use DataDriftOptions.stattest_func"
                          " or DataDriftOptions.per_feature_stattest_func.")
            if callable(self.feature_stattest_func) or isinstance(self.feature_stattest_func, (StatTest, str)):
                return self.feature_stattest_func
            if isinstance(self.feature_stattest_func, dict):
                return self.feature_stattest_func.get(feature_name, default)
            return default
        func = default if self.stattest is None else self.stattest
        if feature_type == "cat":
            type_func = self.cat_stattest
        elif feature_type == "num":
            type_func = self.num_stattest
        else:
            raise ValueError(f"Unexpected feature type {feature_type}.")
        func = func if type_func is None else type_func
        if self.per_feature_stattest is None:
            return func
        return self.per_feature_stattest.get(feature_name, func)
