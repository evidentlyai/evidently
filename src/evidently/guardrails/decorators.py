import inspect
from functools import wraps
from typing import List
from typing import Union

from evidently.guardrails.core import GuardrailBase
from evidently.guardrails.core import validate_guards

try:
    import tracely

    tracely_installed = True
except ImportError:
    tracely_installed = False


def guard(guard: Union[GuardrailBase, List[GuardrailBase]], input_arg: str = "input"):
    def decorator(func):
        sig = inspect.signature(func)

        @wraps(func)
        def wrapper(*args, **kwargs):
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()
            if input_arg not in bound.arguments:
                raise Exception(f"{input_arg} is not a valid argument")
            if isinstance(guard, list):
                if tracely_installed and tracely.get_current_span():
                    tracely.get_current_span().set_context_value("evidently.guardrails", guard)
                validate_guards(bound.arguments[input_arg], guard)
            else:
                if tracely_installed and tracely.get_current_span():
                    tracely.get_current_span().set_context_value("evidently.guardrails", [guard])
                guard.validate(bound.arguments[input_arg])
            return func(*args, **kwargs)

        return wrapper

    return decorator
