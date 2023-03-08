import warnings

import evidently.dashboard.widgets
from evidently.dashboard.widgets import *

__path__ = evidently.dashboard.widgets.__path__  # type: ignore

warnings.warn(
    "'import evidently.widgets' is deprecated, use 'import evidently.dashboard.widgets'"
)
