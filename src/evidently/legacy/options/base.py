from typing import TYPE_CHECKING
from typing import Dict
from typing import List
from typing import Optional
from typing import Type
from typing import TypeVar
from typing import Union

from evidently._pydantic_compat import BaseModel
from evidently.legacy.options import ColorOptions
from evidently.legacy.options.agg_data import DataDefinitionOptions
from evidently.legacy.options.agg_data import RenderOptions
from evidently.legacy.options.option import Option

if TYPE_CHECKING:
    from evidently._pydantic_compat import AbstractSetIntStr
    from evidently._pydantic_compat import DictStrAny
    from evidently._pydantic_compat import MappingIntStrAny
TypeParam = TypeVar("TypeParam", bound=Option)


class Options(BaseModel):
    color: Optional[ColorOptions] = None
    render: Optional[RenderOptions] = None
    custom: Dict[Type[Option], Option] = {}
    data_definition: Optional[DataDefinitionOptions] = None

    @property
    def color_options(self) -> ColorOptions:
        return self.color or ColorOptions()

    @property
    def render_options(self) -> RenderOptions:
        return self.render or RenderOptions()

    @property
    def data_definition_options(self) -> DataDefinitionOptions:
        return self.data_definition or DataDefinitionOptions()

    def get(self, option_type: Type[TypeParam]) -> TypeParam:
        if option_type in _option_cls_mapping:
            res = getattr(self, _option_cls_mapping[option_type])
            if res is None:
                return option_type()
            return res
        if option_type in self.custom:
            return self.custom[option_type]  # type: ignore[return-value]
        for possible_subclass in self.custom.keys():
            if issubclass(possible_subclass, option_type):
                return self.custom[possible_subclass]  # type: ignore[return-value]
        return option_type()

    @classmethod
    def from_list(cls, values: List[Option]) -> "Options":
        kwargs: Dict = {"custom": {}}
        for value in values:
            field = _option_cls_mapping.get(type(value), None)
            if field is not None:
                kwargs[field] = value
            else:
                kwargs["custom"][type(value)] = value
        return Options(**kwargs)

    @classmethod
    def from_any_options(cls, options: "AnyOptions") -> "Options":
        """Options can be provided as Options object, list of Option classes or raw dict"""
        _options = None
        if isinstance(options, dict):
            _options = Options(**options)
        if isinstance(options, Option):
            options = [options]
        if isinstance(options, list):
            _options = Options.from_list(options)
        if isinstance(options, Options):
            _options = options

        return _options or Options()

    def override(self, other: "Options") -> "Options":
        res = Options()
        res.custom = self.custom.copy()
        for key, value in other.custom.items():
            res.custom[key] = value
        for name in self.__fields__:
            if name == "custom":
                continue
            override = getattr(other, name)
            if override is None:
                override = getattr(self, name)
            setattr(res, name, override)

        return res

    def __hash__(self):
        value_pairs = [(f, getattr(self, f)) for f in self.__fields__ if f != "custom"]
        value_pairs.extend(sorted(list(self.custom.items())))
        return hash((type(self),) + tuple(value_pairs))

    def dict(
        self,
        *,
        include: Optional[Union["AbstractSetIntStr", "MappingIntStrAny"]] = None,
        exclude: Optional[Union["AbstractSetIntStr", "MappingIntStrAny"]] = None,
        by_alias: bool = False,
        skip_defaults: Optional[bool] = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
    ) -> "DictStrAny":
        # todo
        # for now custom options will not be saved at all
        # if we want them to be saved, custom field needs to be Dict[str, Option] so it is json-able
        if exclude is None:
            exclude = {"custom"}
        elif isinstance(exclude, set):
            exclude.add("custom")
        elif isinstance(exclude, dict):
            exclude["custom"] = False
        else:
            raise TypeError("exclude must be either a dict or a set")
        return super().dict(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            skip_defaults=skip_defaults,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
        )


_option_cls_mapping = {field.type_: name for name, field in Options.__fields__.items()}

AnyOptions = Union[Options, Option, dict, List[Option], None]
