from typing import Callable

from evidently.guardrails.core import GuardException
from evidently.guardrails.core import GuardrailBase


class PythonFunction(GuardrailBase):
    def __init__(self, function: Callable[[str], bool]):
        super().__init__()
        self.function = function

    def validate(self, data: str):
        if self.function(data):
            return
        raise GuardException(f"{self.function.__name__} validation failed")
