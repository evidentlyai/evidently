import inspect
from itertools import chain
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Type
from typing import Union

from evidently._pydantic_compat import import_string
from evidently.core.datasets import Descriptor
from evidently.core.datasets import DescriptorTest
from evidently.core.datasets import FeatureDescriptor
from evidently.core.tests import GenericTest
from evidently.legacy.core import ColumnType
from evidently.legacy.descriptors.llm_judges import BaseLLMEval
from evidently.legacy.features.custom_feature import CustomFeature
from evidently.legacy.features.custom_feature import CustomPairColumnFeature
from evidently.legacy.features.custom_feature import CustomSingleColumnFeature
from evidently.legacy.features.generated_features import GeneratedFeatures
from evidently.legacy.features.llm_judge import BaseLLMPromptTemplate
from evidently.legacy.features.llm_judge import Uncertainty
from evidently.legacy.features.text_length_feature import TextLength
from evidently.pydantic_utils import TYPE_ALIASES

SOURCE_FILE = "generated_descriptors.py"

REPLACES = {
    "pandas.core.frame.DataFrame": "DataFrame",
    "evidently.utils.data_preprocessing.DataDefinition": "DataDefinition",
    "pandas.core.series.Series": "Series",
    "evidently.features.llm_judge.Uncertainty": "Uncertainty",
    "evidently.legacy.features.llm_judge.Uncertainty": "Uncertainty",
}

NAME_MAPPING = {
    "open_a_i_feature": "openai_feature",
    "is_valid_j_s_o_n": "is_valid_json",
    "is_valid_s_q_l": "is_valid_sql",
}

SKIP_CLASSES = {CustomFeature, CustomPairColumnFeature, CustomSingleColumnFeature, TextLength}


def _get_type_name(tp: Type):
    if tp.__module__.startswith("typing"):
        return str(tp).replace("typing.", "")
    return tp.__name__
    # return str(tp)


def _get_value_str(value):
    if isinstance(value, str):
        return f'"{value}"'
    return str(value)


def get_args_kwargs(feature_class: Type[GeneratedFeatures]) -> Tuple[Dict[str, str], Dict[str, Tuple[str, str]]]:
    if feature_class.__dict__.get("__init__") is None:
        # get from fields
        args = {
            key: _get_type_name(field.annotation) for key, field in feature_class.__fields__.items() if field.required
        }
        kwargs = {
            key: (_get_type_name(field.annotation), _get_value_str(field.default))
            for key, field in feature_class.__fields__.items()
            if not field.required and key != "type"
        }
        return args, kwargs
    # get from constructor
    sig = inspect.getfullargspec(feature_class.__init__)

    defaults = sig.defaults or tuple()
    args = {a: _get_type_name(sig.annotations.get(a, Any)) for a in sig.args[1 : -len(defaults)]}
    kwargs = {
        a: (_get_type_name(sig.annotations.get(a, Any)), _get_value_str(d))
        for a, d in zip(sig.args[-len(defaults) :], defaults)
    }
    kwonlydefaults = sig.kwonlydefaults or {}
    args.update({k: _get_type_name(sig.annotations.get(k, Any)) for k in sig.kwonlyargs if k not in kwonlydefaults})
    kwargs.update(
        {
            k: (_get_type_name(sig.annotations.get(k, Any)), _get_value_str(kwonlydefaults[k]))
            for k in sig.kwonlyargs
            if k in kwonlydefaults
        }
    )
    return args, kwargs


def create_descriptor_function(feature_class: Type[GeneratedFeatures]):
    class_name = feature_class.__name__
    name = class_name
    # name = cmpx.lower() + re.sub(r"(?<!^)(?=[A-Z])", "_", class_name[len(cmpx) :]).lower()
    name = NAME_MAPPING.get(name, name)
    if name.endswith("Feature"):
        name = name[: -len("Feature")]

    args, kwargs = get_args_kwargs(feature_class)
    display_name_required = "display_name" in args
    has_display_name = display_name_required or "display_name" in kwargs
    if not display_name_required:
        kwargs["alias"] = ("Optional[str]", "None")
        kwargs.pop("display_name", None)
    else:
        args["alias"] = "str"
        args.pop("display_name")
    kwargs["tests"] = ('Optional[List[Union["DescriptorTest", "GenericTest"]]]', "None")
    args_str = ", ".join(f"{a}: {t}" for a, t in args.items())
    if len(kwargs) > 0:
        kwargs_str = ", " + ", ".join(f"{a}: {t} = {d}" for a, (t, d) in kwargs.items())
    else:
        kwargs_str = ""

    class_args = ", ".join(f"{k}={k}" for k in chain(args, kwargs) if k not in ("alias", "tests"))
    if has_display_name:
        class_args += ", display_name=alias"
    res = f"""
def {name}({args_str}{kwargs_str}):
        from {feature_class.__module__} import {feature_class.__name__} as {feature_class.__name__}V1
        feature = {class_name}V1({class_args})
        return FeatureDescriptor(feature=feature, alias=alias, tests=tests)
"""
    for substr, repl in REPLACES.items():
        res = res.replace(substr, repl)
    return res, name


def create_llm_descriptor_functions(feature_class: Type[BaseLLMEval]):
    class_name = feature_class.__name__
    name = class_name
    # name = cmpx.lower() + re.sub(r"(?<!^)(?=[A-Z])", "_", class_name[len(cmpx) :]).lower()
    name = NAME_MAPPING.get(name, name)
    if name.endswith("Feature"):
        name = name[: -len("Feature")]

    args, kwargs = get_args_kwargs(feature_class)  # type: ignore[arg-type]
    kwargs["alias"] = ("Optional[str]", "None")
    kwargs["tests"] = ('Optional[List[Union["DescriptorTest", "GenericTest"]]]', "None")
    has_display_name = kwargs.pop("display_name", None) is not None
    args_str = ", ".join(f"{a}: {t}" for a, t in args.items())
    if len(kwargs) > 0:
        kwargs_str = ", ".join(f"{a}: {t} = {d}" for a, (t, d) in kwargs.items())
        if len(args_str) > 0:
            kwargs_str = ", " + kwargs_str
    else:
        kwargs_str = ""
    class_args = ", ".join(f"{k}={k}" for k in chain(args, kwargs) if k not in ("alias", "tests"))
    if has_display_name:
        class_args += ", display_name=alias"
    res = f"""
def {name}(column_name: str, {args_str}{kwargs_str}):
    from {feature_class.__module__} import {feature_class.__name__} as {feature_class.__name__}V1
    feature = {class_name}V1({class_args}).feature(column_name)
    return FeatureDescriptor(feature=feature, alias=alias, tests=tests)
    """
    for substr, repl in REPLACES.items():
        res = res.replace(substr, repl)
    return res, name


def load_all_subtypes(base_class):
    classpaths = [
        cp for (base, _), cp in TYPE_ALIASES.items() if isinstance(base, type) and issubclass(base, base_class)
    ]
    for cp in classpaths:
        try:
            import_string(cp)
        except ImportError as e:
            raise ImportError(f"Cannot import type {cp}") from e


def main():
    for (base_class, _), classpath in list(sorted(TYPE_ALIASES.items(), key=lambda x: x[0][1])):
        if base_class is GeneratedFeatures:
            import_string(classpath)
    subtypes__ = GeneratedFeatures.__subtypes__()

    srcs = []
    fnames = []
    imports: List[Type] = [
        FeatureDescriptor,
        ColumnType,
        BaseLLMPromptTemplate,
        Any,
        List,
        Optional,
        Dict,
        Uncertainty,
        Type,
        DescriptorTest,
        GenericTest,
        Union,
    ]
    for feature_class in sorted(subtypes__, key=lambda x: x.__name__):
        if inspect.isabstract(feature_class):
            continue
        if feature_class in SKIP_CLASSES:
            continue
        src, fname = create_descriptor_function(feature_class)
        fnames.append(fname)
        srcs.append(src)
        # imports.append(feature_class)
    for llm_feature_class in sorted(BaseLLMEval.__subtypes__(), key=lambda x: x.__name__):
        src, fname = create_llm_descriptor_functions(llm_feature_class)
        fnames.append(fname)
        srcs.append(src)
    with open(Path(__file__).parent / SOURCE_FILE, "w") as f:
        f.write("\n".join(f"from {t.__module__} import {t.__name__}" for t in imports) + "\n\n")
        f.write("\n\n".join(srcs))

    load_all_subtypes(Descriptor)
    print(f"from .{SOURCE_FILE[:-3]} import ({', '.join(fnames)})")
    print("__all__ = [")
    fnames.extend(
        [
            sc.__name__
            for sc in Descriptor.__subtypes__()
            if sc not in (FeatureDescriptor,) and not inspect.isabstract(sc)
        ]
    )
    print("\n".join(f'"{fname}",' for fname in sorted(fnames)))
    print("]")


if __name__ == "__main__":
    main()
