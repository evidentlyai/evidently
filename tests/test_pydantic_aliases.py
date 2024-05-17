import glob
import os
from importlib import import_module
from inspect import isabstract
from typing import Set
from typing import Type
from typing import TypeVar

import evidently
from evidently.pydantic_utils import TYPE_ALIASES
from evidently.pydantic_utils import PolymorphicModel
from evidently.pydantic_utils import get_base_class

T = TypeVar("T")


# todo: deduplicate code
def find_all_subclasses(
    base: Type[T],
    base_module: str = "evidently",
    path: str = os.path.dirname(evidently.__file__),
    include_abstract: bool = False,
) -> Set[Type[T]]:
    classes = set()
    for mod in glob.glob(path + "/**/*.py", recursive=True):
        mod_path = os.path.relpath(mod, path)[:-3]
        mod_name = f"{base_module}." + mod_path.replace("/", ".").replace("\\", ".")
        if mod_name.endswith("__"):
            continue
        module = import_module(mod_name)
        for key, value in module.__dict__.items():
            if isinstance(value, type) and value is not base and issubclass(value, base):
                if not isabstract(value) or include_abstract:
                    classes.add(value)

    return classes


def test_all_aliases_registered():
    not_registered = []

    for cls in find_all_subclasses(PolymorphicModel, include_abstract=True):
        classpath = cls.__get_classpath__()
        typename = cls.__get_type__()
        if classpath == typename:
            # no typename
            continue
        key = (get_base_class(cls), typename)
        if key not in TYPE_ALIASES or TYPE_ALIASES[key] != classpath:
            not_registered.append(cls)

    msg = "\n".join(
        f'register_type_alias({get_base_class(cls).__name__}, "{cls.__get_classpath__()}", "{cls.__get_type__()}")'
        for cls in not_registered
    )
    print(msg)
    assert len(not_registered) == 0, "Not all aliases registered"
