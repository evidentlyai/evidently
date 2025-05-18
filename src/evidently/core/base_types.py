from typing import Union

from pydantic import StrictBool

Label = Union[StrictBool, int, str, None]
