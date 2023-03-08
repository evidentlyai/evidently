import warnings

import evidently.model_profile.sections
from evidently.model_profile.sections import *

__path__ = evidently.model_profile.sections.__path__  # type: ignore

warnings.warn(
    "'import evidently.profile_sections' is deprecated, use 'import evidently.model_profile.sections'"
)
