import warnings

import evidently.dashboard.tabs
from evidently.dashboard.tabs import *

__path__ = evidently.dashboard.tabs.__path__  # type: ignore

warnings.warn(
    "'import evidently.tabs' is deprecated, use 'import evidently.dashboard.tabs'"
)
