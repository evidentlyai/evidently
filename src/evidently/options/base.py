from typing import List
from typing import Optional

from pydantic import BaseModel

from evidently.options import ColorOptions
from evidently.options.option import Option


class Options(BaseModel):
    color: Optional[ColorOptions] = None
    agg_data: bool = False

    @property
    def color_options(self) -> ColorOptions:
        return self.color or ColorOptions()

    @classmethod
    def from_list(cls, values: List[Option]):
        cls_mapping = {field.type_: name for name, field in cls.__fields__.items()}
        kwargs = {}
        for value in values:
            field = cls_mapping.get(type(value), None)
            if field is not None:
                kwargs[field] = value
        return Options(**kwargs)
