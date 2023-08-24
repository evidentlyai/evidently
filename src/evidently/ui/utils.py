import os
from typing import Optional

from fastapi import Header
from fastapi import HTTPException
from typing_extensions import Annotated

SECRET = os.environ.get("EVIDENTLY_SECRET", None)


def set_secret(secret: Optional[str]):
    global SECRET
    SECRET = secret


async def authenticated(evidently_secret: Annotated[Optional[str], Header()] = None):
    if SECRET is not None and evidently_secret != SECRET:
        raise HTTPException(403, "Not allowed")
