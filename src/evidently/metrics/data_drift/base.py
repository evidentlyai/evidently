import abc
import warnings
from dataclasses import dataclass
from typing import Dict
from typing import Generic
from typing import Optional
from typing import TypeVar
from typing import Union

from pydantic import BaseModel
from pydantic import PrivateAttr

from evidently.base_metric import Metric
from evidently.base_metric import MetricResult
from evidently.calculations.stattests import PossibleStatTestType
from evidently.calculations.stattests import StatTest
from evidently.options import DataDriftOptions
from evidently.utils.data_drift_utils import resolve_stattest_threshold

T = TypeVar("T", bound=MetricResult)


class WithDriftOptions(Metric[T], Generic[T], abc.ABC):
    _drift_options: DataDriftOptions
    # todo: fields here are not consistent with DriftOptions, so no common base model
    stattest: Optional[PossibleStatTestType] = None
    cat_stattest: Optional[PossibleStatTestType] = None
    num_stattest: Optional[PossibleStatTestType] = None
    text_stattest: Optional[PossibleStatTestType] = None
    per_column_stattest: Optional[Dict[str, PossibleStatTestType]] = None

    stattest_threshold: Optional[float] = None
    cat_stattest_threshold: Optional[float] = None
    num_stattest_threshold: Optional[float] = None
    text_stattest_threshold: Optional[float] = None
    per_column_stattest_threshold: Optional[Dict[str, float]] = None

    @property
    def drift_options(self):
        return self._drift_options
