import inspect
import json
from abc import ABC
from datetime import datetime
from enum import Enum
from typing import Any
from typing import ForwardRef
from typing import Literal
from typing import Type
from typing import Union
from typing import get_args
from typing import get_origin

import pandas as pd
import pytest

from evidently._pydantic_compat import BaseModel
from evidently._pydantic_compat import parse_obj_as
from evidently.core.metric_types import MetricTestResult
from evidently.legacy.model.widget import BaseWidgetInfo
from evidently.legacy.model.widget import TabInfo
from evidently.legacy.utils import NumpyEncoder
from evidently.pydantic_utils import PolymorphicModel
from evidently.pydantic_utils import all_subclasses
from tests.conftest import smart_assert_equal
from tests.multitest.conftest import find_all_subclasses

subclasses = find_all_subclasses(BaseModel)
direct_subclasses = [
    cls for cls in subclasses if cls.__module__.startswith("evidently.core") and cls.__bases__[0] is BaseModel
]

forward_refs = [TabInfo, BaseWidgetInfo, MetricTestResult]


def is_not_abstract(cls):
    """Check if a class is not abstract."""
    return not (inspect.isabstract(cls) or ABC in cls.__bases__)


def _construct_object(cls: Type, path: str = "", visited: set = None) -> Any:
    """Create a non-default value for a given type."""
    if visited is None:
        visited = set()

    # Create a key for this type and path to detect recursion
    if isinstance(cls, ForwardRef):
        type_key = f"ForwardRef({cls.__forward_arg__}):{path}"
    else:
        type_key = f"{cls.__name__}:{path}"
    if type_key in visited:
        # Recursion detected - return a simple value
        if cls is str:
            return "recursive_string"
        elif cls is int:
            return 0
        elif cls is float:
            return 0.0
        elif cls is bool:
            return False
        elif cls is list:
            return []
        elif cls is dict:
            return {}
        elif cls is tuple:
            return ()
        elif cls is set:
            return set()
        else:
            return None

    # Add current type to visited set
    visited.add(type_key)

    try:
        return _construct_object_impl(cls, path, visited)
    finally:
        # Remove from visited set when done
        visited.discard(type_key)


def _construct_object_impl(cls: Type, path: str = "", visited: set = None) -> Any:
    """Implementation of object construction with recursion tracking."""
    # Handle None type
    if cls is type(None) or cls is None:
        return None

    # Handle primitive types with non-default values
    if cls is int:
        return 100
    elif cls is float:
        return 3.14
    elif cls is str:
        return "test_string"
    elif cls is bool:
        return True
    elif cls is bytes:
        return b"test_bytes"

    # Get origin for generic type checking
    origin = get_origin(cls)

    # Handle Union types (including Optional)
    if origin is Union:
        args = get_args(cls)
        # Check if it's Optional (Union[SomeType, None])
        if len(args) == 2 and type(None) in args:
            # Return the non-None type
            non_none_type = args[0] if args[1] is type(None) else args[1]
            return _construct_object(non_none_type, path, visited)
        else:
            # Regular Union - try the first non-None type
            for arg in args:
                if arg is not type(None):
                    return _construct_object(arg, path, visited)
            raise ValueError(f"Union at path '{path}' contains only None types")

    # Handle Literal types
    if origin is Literal:
        args = get_args(cls)
        if args:
            return args[0]  # Return the first literal value
        else:
            raise ValueError(f"Empty Literal at path '{path}'")

    # Handle List types (both generic and non-generic)
    if origin is list or cls is list:
        args = get_args(cls)
        if args:
            element_type = args[0]
            return [_construct_object(element_type, f"{path}[0]", visited)]
        else:
            return ["test_item"]

    # Handle Dict types (both generic and non-generic)
    if origin is dict or cls is dict or str(cls).startswith("typing.Dict"):
        args = get_args(cls)
        if len(args) == 2:
            key_type, value_type = args
            # For Union types as keys, try to find a serializable type
            key_origin = get_origin(key_type)
            if key_origin is Union:
                # For Union types, prefer string or int keys for better serialization
                key_args = get_args(key_type)
                for arg in key_args:
                    if arg is str:
                        key_value = "test_key"
                        break
                    elif arg is int:
                        key_value = 1
                        break
                    elif arg is bool or (hasattr(arg, "__name__") and arg.__name__ == "StrictBool"):
                        # Skip boolean keys to avoid serialization issues
                        continue
                    else:
                        # Fallback to first non-None type
                        key_value = _construct_object(key_args[0], f"{path}.key", visited)
                        break
                else:
                    # If all types were skipped, use string as fallback
                    key_value = "test_key"
            else:
                key_value = _construct_object(key_type, f"{path}.key", visited)
            return {key_value: _construct_object(value_type, f"{path}.value", visited)}
        else:
            # Non-generic dict
            return {"test_key": "test_value"}

    # Handle Tuple types (both generic and non-generic)
    if origin is tuple or cls is tuple:
        args = get_args(cls)
        if args:
            return tuple(_construct_object(arg, f"{path}[{i}]", visited) for i, arg in enumerate(args))
        else:
            return ("test_item",)

    # Handle Set types (both generic and non-generic)
    if origin is set or cls is set:
        args = get_args(cls)
        if args:
            element_type = args[0]
            return {_construct_object(element_type, f"{path}[0]", visited)}
        else:
            return {"test_item"}

    # Handle ForwardRef types
    if isinstance(cls, ForwardRef):
        # Check if we've already seen this ForwardRef to prevent infinite recursion
        forward_ref_key = f"ForwardRef({cls.__forward_arg__})"
        if forward_ref_key in visited:
            # Return a minimal object to avoid recursion
            if cls.__forward_arg__ == "TabInfo":
                return {
                    "id": "recursive_tab",
                    "title": "recursive_title",
                    "widget": {"type": "recursive_type", "title": "recursive_title", "size": 1, "id": "recursive_id"},
                }
            elif cls.__forward_arg__ == "BaseWidgetInfo":
                return {"type": "recursive_type", "title": "recursive_title", "size": 1, "id": "recursive_id"}
            else:
                return []

        # Add to visited set
        visited.add(forward_ref_key)
        try:
            eval_globals = globals().copy()
            eval_globals.update({ref.__name__: ref for ref in forward_refs})
            evaluated = cls._evaluate(eval_globals, locals(), set())
            return _construct_object(evaluated, path, visited)
        finally:
            visited.discard(forward_ref_key)

    # Handle typing.Any
    if cls is Any:
        return "any_value"

    # Handle pandas DataFrame
    if cls is pd.DataFrame:
        return pd.DataFrame({"test_col": [1, 2, 3]})

    # Handle pandas Series
    if cls is pd.Series:
        return pd.Series([1, 2, 3])

    # Handle datetime types
    if cls is datetime:
        return datetime(2023, 1, 1, 12, 0, 0)

    # Handle pydantic types that are similar to built-in types
    if hasattr(cls, "__name__"):
        if cls.__name__ == "StrictBool":
            return True
        elif cls.__name__ == "StrictStr":
            return "strict_string"
        elif cls.__name__ == "StrictInt":
            return 100
        elif cls.__name__ == "StrictFloat":
            return 3.14

    # Handle Enum types
    if isinstance(cls, type) and issubclass(cls, Enum):
        # Return the first enum value
        return list(cls)[0]

    # Handle PolymorphicModel types
    if isinstance(cls, type) and issubclass(cls, PolymorphicModel):
        # Find a non-abstract subclass to construct
        subclasses = all_subclasses(cls)
        non_abstract_subclasses = [subcls for subcls in subclasses if is_not_abstract(subcls)]

        if non_abstract_subclasses:
            # Use the first non-abstract subclass
            concrete_class = non_abstract_subclasses[0]
            return _construct_base_model_object(concrete_class, path, visited)
        else:
            # If no subclasses found, try to construct the class directly if it's not abstract
            if is_not_abstract(cls):
                return _construct_base_model_object(cls, path, visited)
            else:
                raise ValueError(f"No non-abstract subclasses found for PolymorphicModel {cls} at path '{path}'")

    # Handle BaseModel types
    if isinstance(cls, type) and issubclass(cls, BaseModel):
        return _construct_base_model_object(cls, path, visited)

    # For unknown types, raise an error
    raise ValueError(f"I dunno how to construct object at path '{path}' with type {cls}")


def _construct_base_model_object(cls: Type[BaseModel], path: str = "", visited: set = None) -> BaseModel:
    """Recursively create a BaseModel object with non-default values for all fields."""
    # Get all fields from the model
    fields = cls.__fields__ if hasattr(cls, "__fields__") else {}

    # Build kwargs with non-default values for each field
    kwargs = {}
    for field_name, field_info in fields.items():
        # Use outer_type_ if available, otherwise type_
        field_type = getattr(field_info, "outer_type_", field_info.type_)
        field_path = f"{path}.{field_name}" if path else field_name

        kwargs[field_name] = _construct_object(field_type, field_path, visited)

    # Create the instance
    try:
        return cls(**kwargs)
    except Exception as e:
        raise ValueError(f"I dunno how to construct object at path '{path}' with type {cls}: {e}")


@pytest.mark.parametrize("cls", direct_subclasses)
def test_core_object_serialization(cls: Type[BaseModel]):
    obj = _construct_base_model_object(cls, cls.__name__)

    payload = obj.json(cls=NumpyEncoder)

    obj2 = parse_obj_as(cls, json.loads(payload))

    smart_assert_equal(obj, obj2)
