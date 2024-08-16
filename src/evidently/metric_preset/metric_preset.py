import abc
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from evidently.base_metric import BasePreset
from evidently.base_metric import Metric
from evidently.utils.data_preprocessing import DataDefinition


class MetricPreset(BasePreset):
    """Base class for metric presets"""

    @abc.abstractmethod
    def generate_metrics(
        self, data_definition: DataDefinition, additional_data: Optional[Dict[str, Any]]
    ) -> List[Metric]:
        raise NotImplementedError()
