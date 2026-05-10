from typing import Optional

from evidently.legacy.options.option import Option


class RenderOptions(Option):
    raw_data: bool = False
    current_title: str = "Current"
    reference_title: str = "Reference"


class DataDefinitionOptions(Option):
    categorical_features_cardinality: Optional[int] = None
