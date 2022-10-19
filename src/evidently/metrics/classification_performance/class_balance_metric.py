from typing import Dict
from typing import Optional
from typing import Union

import dataclasses

from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.metrics.base_metric import TResult


@dataclasses.dataclass
class ClassificationClassBalanceResult:
    current_label_count: Dict[Union[str, int], int]
    reference_label_count: Optional[Dict[Union[str, int], int]]


class ClassificationClassBalance(Metric[ClassificationClassBalanceResult]):
    def calculate(self, data: InputData) -> ClassificationClassBalanceResult:
        current_count = data.current_data[data.column_mapping.target].value_counts().to_dict()
        reference_count = None
        if data.reference_data is not None:
            reference_count = data.reference_data[data.column_mapping.target].value_counts().to_dict()
        return ClassificationClassBalanceResult(
            current_label_count=current_count,
            reference_label_count=reference_count,
        )
