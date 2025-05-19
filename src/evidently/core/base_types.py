from typing import Union

from evidently._pydantic_compat import StrictBool

Label = Union[StrictBool, int, str, None]
