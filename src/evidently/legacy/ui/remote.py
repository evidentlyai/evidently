"""For backward compatibility with evidently <= 4.9"""

import warnings

from evidently.legacy.ui.workspace import RemoteWorkspace

__all__ = ["RemoteWorkspace"]

warnings.warn(
    "Importing RemoteWorkspace from evidently.legacy.ui.remote is deprecated. Please import from evidently.legacy.ui.workspace",
    DeprecationWarning,
)
