import abc
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from evidently.legacy.base_metric import BasePreset
from evidently.legacy.base_metric import Metric
from evidently.legacy.utils.data_preprocessing import DataDefinition
from evidently.legacy.utils.generators import BaseGenerator

AnyMetric = Union[Metric, BaseGenerator[Metric]]


class MetricPreset(BasePreset):
    """Base class for metric presets"""

    class Config:
        is_base_type = True

    @abc.abstractmethod
    def generate_metrics(
        self, data_definition: DataDefinition, additional_data: Optional[Dict[str, Any]]
    ) -> List[AnyMetric]:
        raise NotImplementedError()
