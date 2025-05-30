from evidently._pydantic_compat import BaseModel


class LLMMessage(BaseModel):
    role: str
    content: str

    @classmethod
    def user(cls, message: str):
        return LLMMessage(role="user", content=message)

    @classmethod
    def system(cls, message: str):
        return LLMMessage(role="system", content=message)
