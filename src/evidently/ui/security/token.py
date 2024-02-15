from typing import Literal

from pydantic import SecretStr

from evidently.ui.security.config import SecurityConfig


class TokenSecurityConfig(SecurityConfig):
    type: Literal["token"] = "token"
    token: SecretStr
