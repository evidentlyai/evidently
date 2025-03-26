from typing import Optional

from pydantic import BaseModel


class Reference(BaseModel):
    relative: Optional[float] = None
    absolute: Optional[float] = None

    def __hash__(self) -> int:
        return hash(self.relative) + hash(self.absolute)
