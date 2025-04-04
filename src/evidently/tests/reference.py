from typing import Optional

from evidently._pydantic_compat import BaseModel


class Reference(BaseModel):
    relative: Optional[float] = None
    absolute: Optional[float] = None

    def __hash__(self) -> int:
        return hash(self.relative) + hash(self.absolute)
