from typing import Any
from typing import Dict

from evidently.pydantic_utils import FrozenBaseModel


class LLMMessage(FrozenBaseModel):
    """A message in an LLM conversation.

    Represents a single message with a role (e.g., "user", "system") and content.
    Used to build conversation histories for LLM interactions.
    """

    role: str
    """Role of the message sender (e.g., "user", "system", "assistant")."""
    content: str
    """Text content of the message."""

    @classmethod
    def user(cls, message: str):
        return LLMMessage(role="user", content=message)

    @classmethod
    def system(cls, message: str):
        return LLMMessage(role="system", content=message)

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_from_tuple

    @classmethod
    def validate_from_tuple(cls, value: Any):
        if isinstance(value, tuple):
            return cls(**{"role": value[0], "content": value[1]})
        if isinstance(value, dict):
            return cls(**value)
        return value


LLMResponse = Dict[str, Any]
