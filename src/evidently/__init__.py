#!/usr/bin/env python
# coding: utf-8
from . import _registry
from ._version import __version__
from ._version import version_info
from .legacy.nbextension import _jupyter_nbextension_paths

__all__ = [
    "__version__",
    "version_info",
    "_jupyter_nbextension_paths",
    "_registry",
]
