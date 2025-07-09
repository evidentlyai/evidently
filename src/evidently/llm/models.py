from typing import Any
from typing import Dict

from evidently.pydantic_utils import FrozenBaseModel


class LLMMessage(FrozenBaseModel):
    role: str
    content: str

    @classmethod
    def user(cls, message: str):
        return LLMMessage(role="user", content=message)

    @classmethod
    def system(cls, message: str):
        return LLMMessage(role="system", content=message)


LLMResponse = Dict[str, Any]
