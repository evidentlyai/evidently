import uuid
from typing import Literal

from evidently._pydantic_compat import BaseModel
from evidently.ui.type_aliases import ZERO_UUID


class SecurityConfig(BaseModel):
    type: str


class NoSecurityConfig(SecurityConfig):
    type: Literal["none"] = "none"

    dummy_user_id: uuid.UUID = ZERO_UUID
    dummy_org_id: uuid.UUID = ZERO_UUID
