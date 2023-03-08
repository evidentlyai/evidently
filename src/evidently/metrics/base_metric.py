from typing import Dict, Optional, Type, Union

from evidently.base_metric import Metric
from evidently.utils.generators import BaseGenerator, make_generator_by_columns


def generate_column_metrics(
    metric_class: Type[Metric],
    columns: Optional[Union[str, list]] = None,
    parameters: Optional[Dict] = None,
    skip_id_column: bool = False,
) -> BaseGenerator:
    """Function for generating metrics for columns"""
    return make_generator_by_columns(
        base_class=metric_class,
        columns=columns,
        parameters=parameters,
        skip_id_column=skip_id_column,
    )
