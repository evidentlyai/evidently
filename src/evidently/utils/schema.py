import sys
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple
from typing import Type
from typing import Union
from typing import no_type_check

import litestar
import msgspec
import typing_inspect
import yaml
from litestar import get
from litestar._openapi.schema_generation import SchemaCreator
from litestar.contrib.pydantic import PydanticSchemaPlugin
from litestar.openapi.spec import Schema
from litestar.serialization import get_serializer
from litestar.typing import FieldDefinition
from typing_inspect import is_generic_type

from evidently._pydantic_compat import SHAPE_DICT
from evidently._pydantic_compat import SHAPE_LIST
from evidently._pydantic_compat import SHAPE_SINGLETON
from evidently._pydantic_compat import ModelField
from evidently._pydantic_compat import create_model
from evidently._pydantic_compat import import_string
from evidently.pydantic_utils import TYPE_ALIASES
from evidently.pydantic_utils import PolymorphicModel
from evidently.pydantic_utils import is_not_abstract
from evidently.ui.service.app import create_app
from evidently.ui.service.app import get_config
from evidently.ui.service.components.base import Component
from evidently.ui.service.components.base import ComponentContext
from evidently.ui.service.datasets.filters import FilterBy
from evidently.ui.service.managers.base import replace_signature


@no_type_check
def _with_shape(cls: Type, model_field: ModelField):
    if model_field.shape == SHAPE_SINGLETON:
        return cls
    if model_field.shape == SHAPE_LIST:
        return List[cls]
    if model_field.shape == SHAPE_DICT:
        return Dict[model_field.key_field.type_, cls]
    raise NotImplementedError(f"Not implemented for shape {model_field.shape}")


def nonabstract_subtypes(cls: Type[PolymorphicModel]) -> Tuple[Type[PolymorphicModel], ...]:
    return tuple([s for s in cls.__subtypes__() if is_not_abstract(s)])


class PolymorphicPydanticSchemaPlugin(PydanticSchemaPlugin):
    """Changes all fields with PolymorphicModel base class types into a union of it's subtypes"""

    @no_type_check
    def to_openapi_schema(self, field_definition: FieldDefinition, schema_creator: SchemaCreator) -> Schema:
        ann = field_definition.annotation

        if is_generic_type(ann):
            ann = typing_inspect.get_origin(ann) or ann
        if isinstance(ann, type) and issubclass(ann, PolymorphicModel) and ann.__is_base_type__():
            subtypes = nonabstract_subtypes(ann)
            if len(subtypes) > 0:
                return schema_creator.for_field_definition(FieldDefinition.from_annotation(Union[subtypes]))
        return super().to_openapi_schema(field_definition, schema_creator)


class _AdditionalModelsComponent(Component):
    def get_route_handlers(self, ctx: ComponentContext):
        @get("/_schema/filterby")
        @replace_signature({}, return_annotation=create_model("Filters", **{"all_set": (FilterBy, ...)}))  # type: ignore[call-overload]
        async def filterby(): ...

        return [filterby]


def litestar_app():
    config = get_config()
    config.additional_components["_schema"] = _AdditionalModelsComponent()
    app = create_app(config)
    app.plugins.openapi = (PolymorphicPydanticSchemaPlugin(),) + app.plugins.openapi
    return app


def sort_schema(schema: Dict[str, Any]):
    def _rec(obj):
        if isinstance(obj, dict):
            for k, v in list(obj.items()):
                if isinstance(v, list) and all(
                    isinstance(o, dict) and any(o) and set(o.keys()).issubset({"$ref", "type", "oneOf"}) for o in v
                ):
                    _rec(v)
                    obj[k] = list(sorted(v, key=lambda x: next(str(x[y]) for y in ("$ref", "type", "oneOf") if y in x)))
                    continue
                if isinstance(v, list) and all(isinstance(o, str) for o in v):
                    obj[k] = list(sorted(v))
                    continue
                _rec(v)
        if isinstance(obj, list):
            for o in obj:
                _rec(o)

    _rec(schema)
    return schema


def write_schema(app: litestar.Litestar, path: str):
    Path(path).write_bytes(dumps_schema(app).encode("utf-8"))


def get_schema(app: litestar.Litestar):
    schema = app.openapi_schema.to_schema()
    return sort_schema(schema)


def dumps_schema(app: litestar.Litestar) -> str:
    schema = get_schema(app)
    return yaml.dump(
        msgspec.to_builtins(schema, enc_hook=get_serializer(app.type_encoders)),
        default_flow_style=False,
        encoding="utf-8",
    ).decode("utf-8")


def import_all_registered():
    for _, classpath in TYPE_ALIASES.items():
        import_string(classpath)


def main():
    path = sys.argv[1]
    import_all_registered()
    app = litestar_app()
    write_schema(app, path)


if __name__ == "__main__":
    main()
