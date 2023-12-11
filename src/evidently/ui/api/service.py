import os
from typing import Optional

from fastapi import APIRouter

import evidently

service_api = APIRouter(prefix="")

# todo: move to config
DEV = True

EVIDENTLY_APPLICATION_NAME = "Evidently UI"


@service_api.get("/version")
async def version():
    result = {
        "application": EVIDENTLY_APPLICATION_NAME,
        "version": evidently.__version__,
    }
    if DEV:
        result["commit"] = get_git_revision_short_hash(os.path.dirname(evidently.__file__))
    return result


def get_git_revision_short_hash(path: str) -> Optional[str]:
    from_env = os.environ.get("GIT_COMMIT")
    if from_env is not None:
        return from_env
    import subprocess

    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=path).decode("ascii").strip()
    except Exception:
        return None
