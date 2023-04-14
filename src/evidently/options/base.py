from typing import List
from typing import Optional
from typing import Union

from pydantic import BaseModel

from evidently.options import ColorOptions
from evidently.options.option import Option


class Options(BaseModel):
    color: Optional[ColorOptions] = None
    agg_data: Optional[bool] = None

    @property
    def color_options(self) -> ColorOptions:
        return self.color or ColorOptions()

    @property
    def agg_data_option(self) -> bool:
        return self.agg_data or False

    @classmethod
    def from_list(cls, values: List[Option]):
        cls_mapping = {field.type_: name for name, field in cls.__fields__.items()}
        kwargs = {}
        for value in values:
            field = cls_mapping.get(type(value), None)
            if field is not None:
                kwargs[field] = value
        return Options(**kwargs)

    @classmethod
    def from_any_options(cls, options: "AnyOptions") -> "Options":
        """Options can be provided as Options object, list of Option classes or raw dict"""
        _options = None
        if isinstance(options, dict):
            _options = Options(**options)
        if isinstance(options, list):
            _options = Options.from_list(options)
        if isinstance(options, Options):
            _options = options

        return _options or Options()

    def override(self, other: "Options") -> "Options":
        res = Options()
        for name in self.__fields__:
            override = getattr(other, name) or getattr(self, name)
            setattr(res, name, override)
        return res


AnyOptions = Union[Options, dict, List[Option], None]
