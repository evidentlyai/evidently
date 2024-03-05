import uuid
from typing import Literal

from evidently._pydantic_compat import BaseModel


class SecurityConfig(BaseModel):
    type: str


class NoSecurityConfig(SecurityConfig):
    type: Literal["none"] = "none"

    dummy_user_id: uuid.UUID = uuid.UUID("00000000-0000-0000-0000-000000000001")
    dummy_org_id: uuid.UUID = uuid.UUID("00000000-0000-0000-0000-000000000002")
