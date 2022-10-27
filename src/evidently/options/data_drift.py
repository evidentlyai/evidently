import warnings
from typing import Dict
from typing import Optional
from typing import Union

from dataclasses import dataclass

from evidently.calculations.stattests import PossibleStatTestType
from evidently.calculations.stattests import StatTest

DEFAULT_NBINSX = 10


@dataclass
class DataDriftOptions:
    """Configuration for Data Drift calculations.

    Attributes:
        confidence: Defines the confidence level for statistical tests.
                    Applies to all features (if passed as float) or certain features (if passed as dictionary).
                    (Deprecated) Use `threshold` to define confidence level for statistical
                     tests as more universal solution.
        threshold: Defines thresholds for statistical tests.
                   Applies to all features (if passed as float) or certain features (if passed as dictionary).
        drift_share: Sets the share of drifting features as a condition for Dataset Drift in the Data Drift report.
        nbinsx: Defines the number of bins in a histogram.
                Applies to all features (if passed as int) or certain features (if passed as dictionary).
        xbins: Defines the boundaries for the size of a specific bin in a histogram.
        feature_stattest_func: Defines a custom statistical test for drift detection in the Data Drift report.
                               Applies to all features (if passed as a function) or individual features (if a dict).
                               (Deprecated) Use `all_features_stattest` or `per_feature_stattest`.
        all_features_stattest: Defines a custom statistical test for drift detection in the Data Drift report
                               for all features.
        cat_features_stattest: Defines a custom statistical test for drift detection in the Data Drift report
                               for categorical features only.
        num_features_stattest: Defines a custom statistical test for drift detection in the Data Drift report
                               for numerical features only.
        per_feature_stattest: Defines a custom statistical test for drift detection in the Data Drift report
                              per feature.
        cat_target_stattest_func: Defines a custom statistical test to detect target drift in category target.
        num_target_stattest_func: Defines a custom statistical test to detect target drift in numeric target.
    """

    confidence: Optional[Union[float, Dict[str, float]]] = None
    threshold: Optional[Union[float, Dict[str, float]]] = None
    drift_share: float = 0.5
    nbinsx: Union[int, Dict[str, int]] = DEFAULT_NBINSX
    xbins: Optional[Dict[str, int]] = None

    feature_stattest_func: Optional[Union[PossibleStatTestType, Dict[str, PossibleStatTestType]]] = None

    all_features_stattest: Optional[PossibleStatTestType] = None
    cat_features_stattest: Optional[PossibleStatTestType] = None
    num_features_stattest: Optional[PossibleStatTestType] = None
    per_feature_stattest: Optional[Dict[str, PossibleStatTestType]] = None

    cat_target_threshold: Optional[float] = None
    num_target_threshold: Optional[float] = None

    cat_target_stattest_func: Optional[PossibleStatTestType] = None
    num_target_stattest_func: Optional[PossibleStatTestType] = None

    def as_dict(self):
        return {
            "confidence": self.confidence,
            "drift_share": self.drift_share,
            "nbinsx": self.nbinsx,
            "xbins": self.xbins,
        }

    def get_threshold(self, feature_name: str) -> Optional[float]:
        if self.confidence is not None and self.threshold is not None:
            raise ValueError("Only DataDriftOptions.confidence or DataDriftOptions.threshold can be set")
        if self.confidence is not None:
            warnings.warn("DataDriftOptions.confidence is deprecated, use DataDriftOptions.threshold instead.")
            if isinstance(self.confidence, float):
                return 1.0 - self.confidence
            if isinstance(self.confidence, dict):
                override = self.confidence.get(feature_name)
                return None if override is None else 1.0 - override
            raise ValueError(f"DataDriftOptions.confidence is incorrect type {type(self.confidence)}")
        if self.threshold is not None:
            if isinstance(self.threshold, float):
                return self.threshold
            if isinstance(self.threshold, dict):
                return self.threshold.get(feature_name)
            raise ValueError(f"DataDriftOptions.threshold is incorrect type {type(self.threshold)}")
        return None

    def get_nbinsx(self, feature_name: str) -> int:
        if isinstance(self.nbinsx, int):
            return self.nbinsx
        if isinstance(self.nbinsx, dict):
            return self.nbinsx.get(feature_name, DEFAULT_NBINSX)
        raise ValueError(f"DataDriftOptions.nbinsx is incorrect type {type(self.nbinsx)}")

    def get_feature_stattest_func(self, feature_name: str, feature_type: str) -> Optional[PossibleStatTestType]:
        if self.feature_stattest_func is not None and any(
            [
                self.all_features_stattest,
                self.cat_features_stattest,
                self.num_features_stattest,
                self.per_feature_stattest,
            ]
        ):
            raise ValueError(
                "Cannot use DataDriftOptions.feature_stattest_func along with any "
                "of DataDriftOptions.cat_stattest_func,"
                " DataDriftOptions.num_stattest_func,"
                " DataDriftOptions.per_feature_stattest_func."
            )
        if self.feature_stattest_func is not None:
            warnings.warn(
                "DataDriftOptions.feature_stattest_func is deprecated use DataDriftOptions.stattest_func"
                " or DataDriftOptions.per_feature_stattest_func."
            )
            if callable(self.feature_stattest_func) or isinstance(self.feature_stattest_func, (StatTest, str)):
                return self.feature_stattest_func
            if isinstance(self.feature_stattest_func, dict):
                return self.feature_stattest_func.get(feature_name)
            return None
        func = None if self.all_features_stattest is None else self.all_features_stattest
        if feature_type == "cat":
            type_func = self.cat_features_stattest
        elif feature_type == "num":
            type_func = self.num_features_stattest
        else:
            raise ValueError(f"Unexpected feature type {feature_type}.")
        func = func if type_func is None else type_func
        if self.per_feature_stattest is None:
            return func
        return self.per_feature_stattest.get(feature_name, func)

    def __hash__(self) -> int:
        """Calculate hash for data drift options - for using in metrics deduplication via dicts."""
        return str(self.as_dict()).__hash__()
