from typing import Callable

from evidently.guardrails.core import GuardException
from evidently.guardrails.core import GuardrailBase


class PythonFunction(GuardrailBase):
    def __init__(self, function: Callable[[str], bool]):
        super().__init__()
        self.function = function

    def name(self) -> str:
        return f"python_function_{self.function.__name__}"

    def validate(self, data: str):
        if self.function(data):
            return
        raise GuardException(self)
