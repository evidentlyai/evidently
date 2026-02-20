import math
from typing import Annotated
from typing import Union

from pydantic import BeforeValidator
from pydantic import StrictBool


def label_validator(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        return value
    if isinstance(value, float) and math.isnan(value):
        return "nan"
    return value


Label = Annotated[Union[StrictBool, int, str, float, None], BeforeValidator(label_validator)]
