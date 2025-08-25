import inspect
from functools import wraps

from evidently.guardrails.core import GuardrailBase


def guard(guard: GuardrailBase, input_arg: str = "input"):
    def decorator(func):
        sig = inspect.signature(func)

        @wraps(func)
        def wrapper(*args, **kwargs):
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()
            if input_arg not in bound.arguments:
                raise Exception(f"{input_arg} is not a valid argument")
            guard.validate(bound.arguments[input_arg])
            return func(*args, **kwargs)

        return wrapper

    return decorator
