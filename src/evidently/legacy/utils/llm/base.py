import dataclasses
from typing import Any
from typing import Dict


@dataclasses.dataclass(unsafe_hash=True, frozen=True)
class LLMMessage:
    role: str
    content: str

    @classmethod
    def user(cls, message: str):
        return LLMMessage("user", message)

    @classmethod
    def system(cls, message: str):
        return LLMMessage("system", message)


LLMResponse = Dict[str, Any]
