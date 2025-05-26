from typing import TYPE_CHECKING

import pydantic

v = 1 if pydantic.__version__.startswith("1") else 2

if v == 1:
    from pydantic import BaseConfig  # type: ignore[assignment]
    from pydantic import BaseModel  # type: ignore[assignment]
    from pydantic import EmailStr  # type: ignore[attr-defined,no-redef]
    from pydantic import Extra  # type: ignore[assignment]
    from pydantic import Field  # type: ignore[assignment]
    from pydantic import PrivateAttr
    from pydantic import SecretStr  # type: ignore[assignment]
    from pydantic import StrictBool  # type: ignore[assignment]
    from pydantic import ValidationError  # type: ignore[assignment]
    from pydantic import create_model  # type: ignore[attr-defined,no-redef]
    from pydantic import parse_obj_as
    from pydantic import root_validator  # type: ignore[attr-defined,no-redef]
    from pydantic import validator
    from pydantic.fields import SHAPE_DICT  # type: ignore[attr-defined,no-redef]
    from pydantic.fields import SHAPE_LIST  # type: ignore[attr-defined,no-redef]
    from pydantic.fields import SHAPE_SET  # type: ignore[attr-defined,no-redef]
    from pydantic.fields import SHAPE_TUPLE  # type: ignore[attr-defined,no-redef]
    from pydantic.fields import ModelField  # type: ignore[attr-defined,no-redef]
    from pydantic.main import ModelMetaclass  # type: ignore[attr-defined,no-redef]
    from pydantic.utils import import_string  # type: ignore[attr-defined,no-redef]
    from pydantic.validators import _VALIDATORS  # type: ignore[attr-defined,no-redef]

    if TYPE_CHECKING:
        from pydantic.main import AbstractSetIntStr  # type: ignore[attr-defined,no-redef]
        from pydantic.main import MappingIntStrAny  # type: ignore[attr-defined,no-redef]
        from pydantic.main import Model  # type: ignore[attr-defined,no-redef]
        from pydantic.typing import DictStrAny  # type: ignore[attr-defined,no-redef]

else:
    from pydantic.v1 import BaseConfig  # type: ignore[assignment,no-redef]
    from pydantic.v1 import BaseModel  # type: ignore[assignment,no-redef]
    from pydantic.v1 import EmailStr  # type: ignore[assignment,no-redef]
    from pydantic.v1 import Extra  # type: ignore[assignment,no-redef]
    from pydantic.v1 import Field  # type: ignore[assignment,no-redef]
    from pydantic.v1 import PrivateAttr  # type: ignore[assignment,no-redef]
    from pydantic.v1 import SecretStr  # type: ignore[assignment,no-redef]
    from pydantic.v1 import StrictBool  # type: ignore[assignment,no-redef]
    from pydantic.v1 import ValidationError  # type: ignore[assignment,no-redef]
    from pydantic.v1 import create_model  # type: ignore[assignment,no-redef]
    from pydantic.v1 import parse_obj_as  # type: ignore[assignment,no-redef]
    from pydantic.v1 import root_validator  # type: ignore[assignment,no-redef]
    from pydantic.v1 import validator  # type: ignore[assignment,no-redef]
    from pydantic.v1.fields import SHAPE_DICT  # type: ignore[assignment,no-redef]
    from pydantic.v1.fields import SHAPE_LIST  # type: ignore[assignment,no-redef]
    from pydantic.v1.fields import SHAPE_SET  # type: ignore[assignment,no-redef]
    from pydantic.v1.fields import SHAPE_TUPLE  # type: ignore[assignment,no-redef]
    from pydantic.v1.fields import ModelField  # type: ignore[assignment,no-redef]
    from pydantic.v1.main import ModelMetaclass  # type: ignore[assignment,no-redef]
    from pydantic.v1.utils import import_string  # type: ignore[assignment,no-redef]
    from pydantic.v1.validators import _VALIDATORS  # type: ignore[assignment,no-redef]

    if TYPE_CHECKING:
        from pydantic.v1.main import AbstractSetIntStr  # type: ignore[assignment,no-redef]
        from pydantic.v1.main import MappingIntStrAny  # type: ignore[assignment,no-redef]
        from pydantic.v1.main import Model  # type: ignore[assignment,no-redef]
        from pydantic.v1.typing import DictStrAny  # type: ignore[assignment,no-redef]

__all__ = [
    "BaseConfig",
    "BaseModel",
    "Field",
    "ValidationError",
    "parse_obj_as",
    "validator",
    "SecretStr",
    "StrictBool",
    "SHAPE_DICT",
    "SHAPE_LIST",
    "SHAPE_SET",
    "SHAPE_TUPLE",
    "ModelField",
    "ModelMetaclass",
    "import_string",
    "_VALIDATORS",
    "Model",
    "MappingIntStrAny",
    "AbstractSetIntStr",
    "DictStrAny",
    "PrivateAttr",
    "Extra",
    "create_model",
    "EmailStr",
    "root_validator",
]
